# 🧠 TDS Virtual Teaching Assistant

An intelligent **Retrieval-Augmented Generation (RAG)**-based **Virtual Teaching Assistant** built to automatically respond to student queries for the **Tools in Data Science (TDS)** course under the **IIT Madras Online B.Sc. Degree in Data Science** program.

---

## 📘 Overview

The **TDS Virtual Teaching Assistant** automates the process of answering student questions on the **TDS Discourse forum** using AI.
It leverages **retrieval-augmented generation (RAG)** to fetch relevant course and forum data and produce context-aware, accurate answers — acting like a human teaching assistant.

---

## 🎯 Objectives

* Build a scalable and intelligent teaching assistant.
* Automate responses to student queries using course and forum data.
* Provide explainable and reference-linked answers.
* Reduce workload for teaching assistants and improve query turnaround time.

---

## 🧩 Features

✅ **Automated Query Response** — Uses embeddings and GPT-based models to generate answers.
✅ **RAG Pipeline** — Fetches most relevant course or Discourse content before responding.
✅ **Multimodal Support** — Handles both text and image-based queries.
✅ **Source Transparency** — Each answer includes verified links to sources.
✅ **API-Based Architecture** — Built using FastAPI for easy integration.
✅ **Health Endpoint** — Provides system and database health status.

---

## 🏗️ System Architecture

**Preprocessing Phase**

* Parses and cleans **Discourse forum posts** and **course markdown content**.
* Splits data into contextual **text chunks** with overlapping windows.
* Generates embeddings using the **OpenAI text-embedding-3-small** model.
* Stores chunks and embeddings in **SQLite (`knowledge_base.db`)**.

**Query Phase**

1. User sends a question (and optionally an image).
2. Query embedding is generated.
3. Similar content is retrieved via cosine similarity.
4. Context is passed to the **GPT-4o-mini** model for generating an accurate, source-linked answer.
5. The API returns a JSON response with `answer` and `sources`.

---

## ⚙️ Technologies Used

| Category          | Tools / Libraries                          |
| ----------------- | ------------------------------------------ |
| **Backend**       | FastAPI, Uvicorn                           |
| **AI / NLP**      | OpenAI GPT-4o-mini, text-embedding-3-small |
| **Data Handling** | SQLite, NumPy, Pandas                      |
| **Web / Async**   | aiohttp, CORS Middleware                   |
| **Parsing**       | BeautifulSoup4, html2text, markdown        |
| **Deployment**    | Render / Hugging Face / Localhost          |
| **Environment**   | Python-dotenv                              |

---

## 📁 Project Structure

```
TDS_Virtual_Teaching_Assistant/
│
├── app.py                # FastAPI-based query API (core logic)
├── preprocess.py         # Data ingestion and embedding creation
├── knowledge_base.db     # SQLite database with embedded chunks
├── .env                  # Contains API key
├── requirements.txt      # Project dependencies
├── gitignore.txt         # Ignored files and directories
└── README.md             # Project documentation
```

---

## 🧠 API Endpoints

| Method   | Endpoint  | Description                                                                            |
| -------- | --------- | -------------------------------------------------------------------------------------- |
| **POST** | `/query`  | Takes a question (and optional image) and returns an AI-generated answer with sources. |
| **GET**  | `/health` | Checks API status, database connection, and embedding counts.                          |

---

## 🔧 Setup Instructions

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Add your API key in `.env`**

   ```bash
   API_KEY="your_api_key_here"
   ```

3. **Run the app**

   ```bash
   uvicorn app:app --reload
   ```

4. **Visit the interactive API UI**
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Example Query

```json
{
  "question": "What is pandas used for in the TDS course?"
}
```

---

## 💡 Example Response

```json
{
  "answer": "Pandas is a Python library used in the Tools in Data Science course for data manipulation and analysis.",
  "links": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/pandas-basics/12345",
      "text": "Introduction to Pandas library and its DataFrame structure."
    }
  ]
}
```

---

## 🔍 Future Improvements

* Add authentication for secure access
* Integrate with IITM LMS portal for personalized help
* Support multilingual question answering
* Expand to other IITM courses

---

## 🖼️ Project Demo

The project is live at:
🌐 [**https://tds-project-1-qt1e.onrender.com/docs#/**](https://tds-project-1-qt1e.onrender.com/docs#/)

### Example Interaction

| **Query** | **Response** |
|----------|--------------|
| **Is this course really very hard?** <br><br> ![Question Example](images/query_example.png) | **Yes, this course is considered very hard. Feedback from students indicates that it has become significantly more difficult compared to previous terms, with many students struggling to pass. The course requires more time than typical 3-credit courses, and assessments are described as challenging, particularly the remote open exams and the final in-person exam. Additionally, the unpredictability of grading by LLMs adds to the difficulty level.** <br><br> ![Answer Example](images/response_example.png) |

> The assistant retrieves relevant course and discourse content to answer queries intelligently.

---

## 👨‍💻 Author

**Shreshta Sutar**
🎓 Student — *IIT Madras Online Degree in Data Science*
💡 Interests: AI, NLP, and Education Technology
🔗 [GitHub](https://github.com/ShreshtaSutar) • [LinkedIn](https://linkedin.com/in/) *(add your link)*

---

## 🧾 License

This project is licensed under the **MIT License**.
See [LICENSE](LICENSE) for more details.

---

## ⭐ Acknowledgements

Special thanks to the **IIT Madras Online Degree TDS Team** and the **Discourse community** for providing valuable data that powers this project.

---
