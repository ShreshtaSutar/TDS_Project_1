# preprocess.py
import os
import json
import sqlite3
import re
from bs4 import BeautifulSoup
import html2text
from tqdm import tqdm
import aiohttp
import asyncio
import argparse
import markdown
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
DISCOURSE_DIR = "downloaded_threads"
MARKDOWN_DIR = "markdown_files"
DB_PATH = "knowledge_base.db"

# Ensure directories exist
os.makedirs(DISCOURSE_DIR, exist_ok=True)
os.makedirs(MARKDOWN_DIR, exist_ok=True)

# Chunking parameters
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Get API key from environment variable
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    logger.error("API_KEY environment variable not set. Please set it before running.")

# Create a connection to the SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        logger.info(f"Connected to SQLite database at {DB_PATH}")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return None

# Create the database tables
def create_tables(conn):
    try:
        cursor = conn.cursor()
        
        # Table for Discourse posts chunks
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS discourse_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            topic_id INTEGER,
            topic_title TEXT,
            post_number INTEGER,
            author TEXT,
            created_at TEXT,
            likes INTEGER,
            chunk_index INTEGER,
            content TEXT,
            url TEXT,
            embedding BLOB
        )
        ''')
        
        # Table for markdown document chunks
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS markdown_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_title TEXT,
            original_url TEXT,
            downloaded_at TEXT,
            chunk_index INTEGER,
            content TEXT,
            embedding BLOB
        )
        ''')
        
        conn.commit()
        logger.info("Database tables created successfully")
    except sqlite3.Error as e:
        logger.error(f"Error creating tables: {e}")

# Split text into overlapping chunks with improved chunking
def create_chunks(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    if not text:
        return []
    
    chunks = []
    
    # Clean up whitespace and newlines, preserving meaningful paragraph breaks
    text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with single
    text = re.sub(r'\s+', ' ', text)   # Replace multiple spaces with single
    text = text.strip()
    
    # If text is very short, return it as a single chunk
    if len(text) <= chunk_size:
        return [text]
    
    # Split text by paragraphs for more meaningful chunks
    paragraphs = text.split('\n')
    current_chunk = ""
    
    for i, para in enumerate(paragraphs):
        # If this paragraph alone exceeds chunk size, we need to split it further
        if len(para) > chunk_size:
            # If we have content in the current chunk, store it first
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            
            # Split the paragraph into sentences
            sentences = re.split(r'(?<=[.!?])\s+', para)
            sentence_chunk = ""
            
            for sentence in sentences:
                # If single sentence exceeds chunk size, split by chunks with overlap
                if len(sentence) > chunk_size:
                    # If we have content in the sentence chunk, store it first
                    if sentence_chunk:
                        chunks.append(sentence_chunk.strip())
                        sentence_chunk = ""
                    
                    # Process the long sentence in chunks
                    for j in range(0, len(sentence), chunk_size - chunk_overlap):
                        sentence_part = sentence[j:j + chunk_size]
                        if sentence_part:
                            chunks.append(sentence_part.strip())
                
                # If adding this sentence would exceed chunk size, save current and start new
                elif len(sentence_chunk) + len(sentence) > chunk_size and sentence_chunk:
                    chunks.append(sentence_chunk.strip())
                    sentence_chunk = sentence
                else:
                    # Add to current sentence chunk
                    if sentence_chunk:
                        sentence_chunk += " " + sentence
                    else:
                        sentence_chunk = sentence
            
            # Add any remaining sentence chunk
            if sentence_chunk:
                chunks.append(sentence_chunk.strip())
            
        # Normal paragraph handling - if adding would exceed chunk size
        elif len(current_chunk) + len(para) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Start new chunk with this paragraph
            current_chunk = para
        else:
            # Add to current chunk
            if current_chunk:
                current_chunk += " " + para
            else:
                current_chunk = para
    
    # Add the last chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    # Verify we have chunks and apply overlap between chunks
    if chunks:
        # Create new chunks list with proper overlap
        overlapped_chunks = [chunks[0]]
        
        for i in range(1, len(chunks)):
            prev_chunk = chunks[i-1]
            current_chunk = chunks[i]
            
            # If the previous chunk ends with a partial sentence, find where it begins
            if len(prev_chunk) > chunk_overlap:
                # Find a good breaking point for overlap
                overlap_start = max(0, len(prev_chunk) - chunk_overlap)
                # Try to find sentence boundary
                sentence_break = prev_chunk.rfind('. ', overlap_start)
                if sentence_break != -1 and sentence_break > overlap_start:
                    overlap = prev_chunk[sentence_break+2:]
                    if overlap and not current_chunk.startswith(overlap):
                        current_chunk = overlap + " " + current_chunk
                
            overlapped_chunks.append(current_chunk)
        
        return overlapped_chunks
    
    # If no chunks were created but text exists, return it as a single chunk
    if text:
        return [text]
    
    return []

# Clean HTML content from Discourse posts
def clean_html(html_content):
    if not html_content:
        return ""
    
    # Use BeautifulSoup to parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    
    # Convert to text and clean up whitespace
    text = soup.get_text(separator=' ')
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Parse Discourse JSON files
def process_discourse_files(conn):
    cursor = conn.cursor()
    
    # Check if table exists and has data
    cursor.execute("SELECT COUNT(*) FROM discourse_chunks")
    count = cursor.fetchone()[0]
    if count > 0:
        logger.info(f"Found {count} existing discourse chunks in database, skipping processing")
        return
    
    discourse_files = [f for f in os.listdir(DISCOURSE_DIR) if f.endswith('.json')]
    logger.info(f"Found {len(discourse_files)} Discourse JSON files to process")
    
    total_chunks = 0
    
    for file_name in tqdm(discourse_files, desc="Processing Discourse files"):
        try:
            file_path = os.path.join(DISCOURSE_DIR, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Extract topic information
                topic_id = data.get('id')
                topic_title = data.get('title', '')
                topic_slug = data.get('slug', '')
                
                # Process each post in the topic
                posts = data.get('post_stream', {}).get('posts', [])
                
                for post in posts:
                    post_id = post.get('id')
                    post_number = post.get('post_number')
                    author = post.get('username', '')
                    created_at = post.get('created_at', '')
                    likes = post.get('like_count', 0)
                    html_content = post.get('cooked', '')
                    
                    # Clean HTML content
                    clean_content = clean_html(html_content)
                    
                    # Skip if content is too short
                    if len(clean_content) < 20:
                        continue
                    
                    # Create post URL with proper format
                    url = f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_slug}/{topic_id}/{post_number}"
                    
                    # Split content into chunks
                    chunks = create_chunks(clean_content)
                    
                    # Store chunks in database
                    for i, chunk in enumerate(chunks):
                        cursor.execute('''
                        INSERT INTO discourse_chunks 
                        (post_id, topic_id, topic_title, post_number, author, created_at, likes, chunk_index, content, url, embedding)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (post_id, topic_id, topic_title, post_number, author, created_at, likes, i, chunk, url, None))
                        total_chunks += 1
            
            conn.commit()
        except Exception as e:
            logger.error(f"Error processing file {file_name}: {e}")
    
    logger.info(f"Finished processing Discourse files. Created {total_chunks} chunks.")

# Parse markdown files
def process_markdown_files(conn):
    cursor = conn.cursor()
    
    # Check if table exists and has data
    cursor.execute("SELECT COUNT(*) FROM markdown_chunks")
    count = cursor.fetchone()[0]
    if count > 0:
        logger.info(f"Found {count} existing markdown chunks in database, skipping processing")
        return
    
    markdown_files = [f for f in os.listdir(MARKDOWN_DIR) if f.endswith('.md')]
    logger.info(f"Found {len(markdown_files)} Markdown files to process")
    
    total_chunks = 0
    
    for file_name in tqdm(markdown_files, desc="Processing Markdown files"):
        try:
            file_path = os.path.join(MARKDOWN_DIR, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Extract metadata from frontmatter
                title = ""
                original_url = ""
                downloaded_at = ""
                
                # Extract metadata from frontmatter if present
                frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
                if frontmatter_match:
                    frontmatter = frontmatter_match.group(1)
                    
                    # Extract title
                    title_match = re.search(r'title: "(.*?)"', frontmatter)
                    if title_match:
                        title = title_match.group(1)
                    
                    # Extract original URL
                    url_match = re.search(r'original_url: "(.*?)"', frontmatter)
                    if url_match:
                        original_url = url_match.group(1)
                    
                    # Extract downloaded at timestamp
                    date_match = re.search(r'downloaded_at: "(.*?)"', frontmatter)
                    if date_match:
                        downloaded_at = date_match.group(1)
                    
                    # Remove frontmatter from content
                    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
                
                # Split content into chunks
                chunks = create_chunks(content)
                
                # Store chunks in database
                for i, chunk in enumerate(chunks):
                    cursor.execute('''
                    INSERT INTO markdown_chunks 
                    (doc_title, original_url, downloaded_at, chunk_index, content, embedding)
                    VALUES (?, ?, ?, ?, ?, NULL)
                    ''', (title, original_url, downloaded_at, i, chunk))
                    total_chunks += 1
            
            conn.commit()
        except Exception as e:
            logger.error(f"Error processing file {file_name}: {e}")
    
    logger.info(f"Finished processing Markdown files. Created {total_chunks} chunks.")

# Function to create embeddings using aipipe proxy with improved error handling and retries
async def create_embeddings(api_key):
    if not api_key:
        logger.error("API_KEY environment variable not set. Cannot create embeddings.")
        return
        
    conn = create_connection()
    cursor = conn.cursor()
    
    # Get discourse chunks without embeddings
    cursor.execute("SELECT id, content FROM discourse_chunks WHERE embedding IS NULL")
    discourse_chunks = cursor.fetchall()
    logger.info(f"Found {len(discourse_chunks)} discourse chunks to embed")
    
    # Get markdown chunks without embeddings
    cursor.execute("SELECT id, content FROM markdown_chunks WHERE embedding IS NULL")
    markdown_chunks = cursor.fetchall()
    logger.info(f"Found {len(markdown_chunks)} markdown chunks to embed")
    
    # Function to handle long texts by breaking them into multiple embeddings
    async def handle_long_text(session, text, record_id, is_discourse=True, max_retries=3):
        # Model limit is 8191 tokens for text-embedding-3-small
        max_chars = 8000  # Conservative limit to stay under token limit
        
        # If text is within limit, embed it directly
        if len(text) <= max_chars:
            return await embed_text(session, text, record_id, is_discourse, max_retries)
        
        # For long texts, we need to split and create multiple embeddings
        logger.info(f"Text exceeds embedding limit for {record_id}: {len(text)} chars. Creating multiple embeddings.")
        
        # First, get the overlapping subchunks
        overlap = 200  # Small overlap between subchunks for continuity
        subchunks = []
        
        # Create overlapping subchunks
        for i in range(0, len(text), max_chars - overlap):
            end = min(i + max_chars, len(text))
            subchunk = text[i:end]
            if subchunk:
                subchunks.append(subchunk)
        
        logger.info(f"Split into {len(subchunks)} subchunks for embedding")
        
        # Create embeddings for all subchunks
        embeddings = []
        for i, subchunk in enumerate(subchunks):
            logger.info(f"Embedding subchunk {i+1}/{len(subchunks)} for {record_id}")
            success = await embed_text(
                session, 
                subchunk, 
                record_id,
                is_discourse, 
                max_retries,
                f"part_{i+1}_of_{len(subchunks)}"  # Identify this as part of a multi-part embedding
            )
            if not success:
                logger.error(f"Failed to embed subchunk {i+1}/{len(subchunks)} for {record_id}")
        
        return True
    
    # Function to embed a single text with retry mechanism
    async def embed_text(session, text, record_id, is_discourse=True, max_retries=3, part_id=None):
        retries = 0
        while retries < max_retries:
            try:
                # Call the embedding API through aipipe proxy
                url = "https://aipipe.org/openai/v1/embeddings"
                headers = {
                    "Authorization": api_key,
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "text-embedding-3-small",
                    "input": text
                }
                
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        embedding = result["data"][0]["embedding"]
                        
                        # Convert embedding to binary blob
                        embedding_blob = json.dumps(embedding).encode()
                        
                        # Update the database - handle multi-part embeddings differently
                        if part_id:
                            # For multi-part embeddings, we create additional records
                            if is_discourse:
                                # First, get the original chunk data to duplicate
                                cursor.execute("""
                                SELECT post_id, topic_id, topic_title, post_number, author, created_at, 
                                       likes, chunk_index, content, url FROM discourse_chunks 
                                WHERE id = ?
                                """, (record_id,))
                                original = cursor.fetchone()
                                
                                if original:
                                    # Create a new record with the subchunk and its embedding
                                    cursor.execute("""
                                    INSERT INTO discourse_chunks 
                                    (post_id, topic_id, topic_title, post_number, author, created_at, 
                                     likes, chunk_index, content, url, embedding)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    """, (
                                        original["post_id"], 
                                        original["topic_id"], 
                                        original["topic_title"], 
                                        original["post_number"],
                                        original["author"], 
                                        original["created_at"], 
                                        original["likes"], 
                                        f"{original['chunk_index']}_{part_id}",  # Append part_id to chunk_index
                                        text, 
                                        original["url"], 
                                        embedding_blob
                                    ))
                            else:
                                # Handle markdown chunks similarly
                                cursor.execute("""
                                SELECT doc_title, original_url, downloaded_at, chunk_index FROM markdown_chunks 
                                WHERE id = ?
                                """, (record_id,))
                                original = cursor.fetchone()
                                
                                if original:
                                    cursor.execute("""
                                    INSERT INTO markdown_chunks 
                                    (doc_title, original_url, downloaded_at, chunk_index, content, embedding)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                    """, (
                                        original["doc_title"],
                                        original["original_url"],
                                        original["downloaded_at"],
                                        f"{original['chunk_index']}_{part_id}",  # Append part_id to chunk_index
                                        text,
                                        embedding_blob
                                    ))
                        else:
                            # For regular embeddings, just update the existing record
                            if is_discourse:
                                cursor.execute(
                                    "UPDATE discourse_chunks SET embedding = ? WHERE id = ?",
                                    (embedding_blob, record_id)
                                )
                            else:
                                cursor.execute(
                                    "UPDATE markdown_chunks SET embedding = ? WHERE id = ?",
                                    (embedding_blob, record_id)
                                )
                        
                        conn.commit()
                        return True
                    elif response.status == 429:  # Rate limit error
                        error_text = await response.text()
                        logger.warning(f"Rate limit reached, retrying after delay (retry {retries+1}): {error_text}")
                        await asyncio.sleep(5 * (retries + 1))  # Exponential backoff
                        retries += 1
                    else:
                        error_text = await response.text()
                        logger.error(f"Error embedding text (status {response.status}): {error_text}")
                        return False
            except Exception as e:
                logger.error(f"Exception embedding text: {e}")
                retries += 1
                await asyncio.sleep(3 * retries)  # Wait before retry
        
        logger.error(f"Failed to embed text after {max_retries} retries")
        return False
    
    # Process in smaller batches to avoid rate limits
    batch_size = 10
    async with aiohttp.ClientSession() as session:
        # Process discourse chunks
        for i in range(0, len(discourse_chunks), batch_size):
            batch = discourse_chunks[i:i+batch_size]
            tasks = [handle_long_text(session, text, record_id, True) for record_id, text in batch]
            results = await asyncio.gather(*tasks)
            logger.info(f"Embedded discourse batch {i//batch_size + 1}/{(len(discourse_chunks) + batch_size - 1)//batch_size}: {sum(results)}/{len(batch)} successful")
            
            # Sleep to avoid rate limits
            if i + batch_size < len(discourse_chunks):
                await asyncio.sleep(2)
        
        # Process markdown chunks
        for i in range(0, len(markdown_chunks), batch_size):
            batch = markdown_chunks[i:i+batch_size]
            tasks = [handle_long_text(session, text, record_id, False) for record_id, text in batch]
            results = await asyncio.gather(*tasks)
            logger.info(f"Embedded markdown batch {i//batch_size + 1}/{(len(markdown_chunks) + batch_size - 1)//batch_size}: {sum(results)}/{len(batch)} successful")
            
            # Sleep to avoid rate limits
            if i + batch_size < len(markdown_chunks):
                await asyncio.sleep(2)
    
    conn.close()
    logger.info("Finished creating embeddings")

# Main function
async def main():
    global CHUNK_SIZE, CHUNK_OVERLAP
    
    parser = argparse.ArgumentParser(description="Preprocess Discourse posts and markdown files for RAG system")
    parser.add_argument("--api-key", help="API key for aipipe proxy (if not provided, will use API_KEY environment variable)")
    parser.add_argument("--chunk-size", type=int, default=CHUNK_SIZE, help=f"Size of text chunks (default: {CHUNK_SIZE})")
    parser.add_argument("--chunk-overlap", type=int, default=CHUNK_OVERLAP, help=f"Overlap between chunks (default: {CHUNK_OVERLAP})")
    args = parser.parse_args()
    
    # Get API key from arguments or environment variable
    api_key = args.api_key or API_KEY
    if not api_key:
        logger.error("API key not provided. Please provide it via --api-key argument or API_KEY environment variable.")
        return
    
    CHUNK_SIZE = args.chunk_size
    CHUNK_OVERLAP = args.chunk_overlap
    
    logger.info(f"Using chunk size: {CHUNK_SIZE}, chunk overlap: {CHUNK_OVERLAP}")
    
    # Create database connection
    conn = create_connection()
    if conn is None:
        return
    
    # Create tables
    create_tables(conn)
    
    # Process files
    process_discourse_files(conn)
    process_markdown_files(conn)
    
    # Create embeddings
    await create_embeddings(api_key)
    
    # Close connection
    conn.close()
    logger.info("Preprocessing complete")

if __name__ == "__main__":
    asyncio.run(main())