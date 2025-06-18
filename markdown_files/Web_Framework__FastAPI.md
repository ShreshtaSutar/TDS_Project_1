---
title: "Web Framework: FastAPI"
original_url: "https://tds.s-anand.net/#/fastapi?id=web-framework-fastapi"
downloaded_at: "2025-06-12T14:58:48.582431"
---

[Web Framework: FastAPI](#/fastapi?id=web-framework-fastapi)
------------------------------------------------------------

[FastAPI](https://fastapi.tiangolo.com/) is a modern Python web framework for building APIs with automatic interactive documentation. It’s fast, easy to use, and designed for building production-ready REST APIs.

Here’s a minimal FastAPI app, `app.py`:

```
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn",
# ]
# ///

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)Copy to clipboardErrorCopied
```

Run this with `uv run app.py`.

1. **Handle errors by raising HTTPException**

   ```
   from fastapi import HTTPException

   async def get_item(item_id: int):
       if not valid_item(item_id):
           raise HTTPException(
               status_code=404,
               detail=f"Item {item_id} not found"
           )Copy to clipboardErrorCopied
   ```
2. **Use middleware for logging**

   ```
   from fastapi import Request
   import time

   @app.middleware("http")
   async def add_timing(request: Request, call_next):
       start = time.time()
       response = await call_next(request)
       response.headers["X-Process-Time"] = str(time.time() - start)
       return responseCopy to clipboardErrorCopied
   ```

Tools:

* [FastAPI CLI](https://fastapi.tiangolo.com/tutorial/fastapi-cli/): Project scaffolding
* [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation
* [SQLModel](https://sqlmodel.tiangolo.com/): SQL databases
* [FastAPI Users](https://fastapi-users.github.io/): Authentication

Watch this FastAPI Course for Beginners (64 min):

[![FastAPI Course for Beginners (64 min)](https://i.ytimg.com/vi_webp/tLKKmouUams/sddefault.webp)](https://youtu.be/tLKKmouUams)

[Previous

REST APIs](#/rest-apis)

[Next

Authentication: Google Auth](#/google-auth)