---
title: "Markdown"
original_url: "https://tds.s-anand.net/#/markdown?id=documentation-markdown"
downloaded_at: "2025-06-12T14:50:14.420210"
---

[Documentation: Markdown](#/markdown?id=documentation-markdown)
---------------------------------------------------------------

Markdown is a lightweight markup language for creating formatted text using a plain-text editor. It’s the standard for documentation in software projects and data science notebooks.

Watch this introduction to Markdown (19 min):

[![Markdown Crash Course (19 min)](https://i.ytimg.com/vi_webp/HUBNt18RFbo/sddefault.webp)](https://youtu.be/HUBNt18RFbo)

Common Markdown syntax:

```
# Heading 1
## Heading 2

**bold** and *italic*

- Bullet point
- Another point
  - Nested point

1. Numbered list
2. Second item

[Link text](https://url.com)
![Image alt](image.jpg)

```python
# Code block
def hello():
    print("Hello")
```

> BlockquoteCopy to clipboardErrorCopied
```

There is also a [GitHub Flavored Markdown](https://github.github.com/gfm/) standard which is popular. This includes extensions like:

```
- [ ] Incomplete task
- [x] Completed task

~~Strikethrough~~

Tables:

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |
Copy to clipboardErrorCopied
```

Tools for working with Markdown:

* [markdown2](https://pypi.org/project/markdown2/): Python library to convert Markdown to HTML
* [markdownlint](https://github.com/DavidAnson/markdownlint): Linting
* [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one): VS Code extension
* [pandoc](https://pandoc.org/): Convert between formats

[Previous

2. Deployment Tools](#/deployment-tools)

[Next

Images: Compression](#/image-compression)