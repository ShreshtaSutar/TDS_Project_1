---
title: "LLM Image Generation"
original_url: "https://tds.s-anand.net/#/llm-image-generation?id=simple-image-editing"
downloaded_at: "2025-06-12T14:51:37.816229"
---

[Gemini Flash Experimental Image Generation and Editing APIs](#/llm-image-generation?id=gemini-flash-experimental-image-generation-and-editing-apis)
----------------------------------------------------------------------------------------------------------------------------------------------------

In March 2025, Google introduced native image generation and editing capabilities in the Gemini 2.0 Flash Experimental model. You can now generate and iteratively edit images via a single REST endpoint ([Experiment with Gemini 2.0 Flash native image generation](https://developers.googleblog.com/en/experiment-with-gemini-20-flash-native-image-generation/), [Generate images | Gemini API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/image-generation)).

[![How to use Latest Gemini 2.0 Native Image Generation with API? (9 min)](https://i.ytimg.com/vi_webp/wgs4UYx6quY/sddefault.webp)](https://youtu.be/wgs4UYx6quY) ([How to use Latest Gemini 2.0 Native Image Generation with API?](https://www.youtube.com/watch?v=wgs4UYx6quY))

### [Simple image generation](#/llm-image-generation?id=simple-image-generation)

To generate a basic image, send a POST request to the `generateContent` method:

```
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
    "contents": [{ "parts": [{ "text": "A serene landscape of rolling hills at sunrise, digital art" }] }],
    "generationConfig": { "responseModalities": ["TEXT", "IMAGE"] }
  }' | jq -r '.candidates[].content.parts[] | select(.inlineData) | .inlineData.data' | base64 --decode > image.pngCopy to clipboardErrorCopied
```

Replace `$GEMINI_API_KEY` with your key. ([Gemini API | Google AI for Developers](https://ai.google.dev/gemini-api/docs))

### [Generation options](#/llm-image-generation?id=generation-options)

You can tweak the output with these `generationConfig` parameters:

* `responseModalities`: Modalities to return (`TEXT`, `IMAGE`).
* `temperature` (0.0–2.0): Controls randomness (default 1.0).
* `topP` (0.0–1.0): Nucleus sampling threshold.
* `topK`: Token selection cutoff.
* `maxOutputTokens`: Max tokens for text parts.
* `stopSequences`: Sequences to end generation.
* `seed`: For reproducibility.

```
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
    "contents": [{ "parts": [{ "text": "A futuristic city skyline at dusk, neon lights" }] }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "temperature": 0.7,
      "topP": 0.9,
      "maxOutputTokens": 1024
    }
  }' | jq -r '.candidates[].content.parts[] | select(.inlineData) | .inlineData.data' | base64 --decode > image.pngCopy to clipboardErrorCopied
```

[Image Generation Docs](https://ai.google.dev/gemini-api/docs/image-generation)

### [Simple image editing](#/llm-image-generation?id=simple-image-editing)

To edit an existing image, include it in the `contents` as `inlineData` (base64-encoded):

```
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "contents": [{
        "parts":[
            {"text": "Replace the background with a starry night sky"},
            {"inline_data": {"mime_type":"image/jpeg", "data": "'$(base64 -w 0 cat.jpg)'"}}
        ]
      }],
      "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }' | jq -r '.candidates[].content.parts[] | select(.inlineData) | .inlineData.data' | base64 --decode > image.pngCopy to clipboardErrorCopied
```

[Image Editing Docs](https://ai.google.dev/gemini-api/docs/image-generation)

### [Editing options](#/llm-image-generation?id=editing-options)

Editing requests support:

* `inlineData`: Embed raw image bytes.
* `fileData`: Reference public URLs.
* All `generationConfig` options listed above.
* `safetySettings`: Per-request safety rules.
* Multi-turn edits by repeating `contents` in conversation history.

### [Costs and optimization](#/llm-image-generation?id=costs-and-optimization)

Gemini 2.0 Flash Experimental uses token-based billing:

* **Input** (text/image/video): free tier, then $0.10 per 1M tokens.
* **Output** (text/image): free tier, then $0.40 per 1M tokens.
* **Per-image flat cost** for Pro models: ~$0.001315 /image ([Gemini Developer API Pricing | Gemini API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/pricing), [Solved: Re: Outdated Gemini Pro image pricing? By tile, or…](https://www.googlecloudcommunity.com/gc/AI-ML/Outdated-Gemini-Pro-image-pricing-By-tile-or-by-image/m-p/813755)).

To optimize:

* Use smaller image sizes by setting `responseMimeType`.
* Cache or reuse prompts with `cachedContent`.
* Lower `candidateCount` or `temperature` for fewer tokens.

[OpenAI gpt-image-1 Model for Image Generation and Editing](#/llm-image-generation?id=openai-gpt-image-1-model-for-image-generation-and-editing)
------------------------------------------------------------------------------------------------------------------------------------------------

OpenAI’s GPT Image 1 (`gpt-image-1`) is a state-of-the-art multimodal model released on April 23, 2025, for high-fidelity image creation and editing.

[![OpenAI’s New GPT Image Model API in 5 Minutes (5 min)](https://i.ytimg.com/vi_webp/k-G71JZA75A/sddefault.webp)](https://youtu.be/k-G71JZA75A)

### [Simple image generation](#/llm-image-generation?id=simple-image-generation-1)

Use the Image Generations endpoint:

```
curl 'https://api.openai.com/v1/images/generations' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-image-1",
    "prompt": "A whimsical illustration of a cat playing chess",
    "n": 1,
    "size": "1024x1024"
  }' > image.pngCopy to clipboardErrorCopied
```

([Generate Image | OpenAI API - Postman](https://www.postman.com/devrel/openai/request/riub8s3/generate-image))

### [Generation options](#/llm-image-generation?id=generation-options-1)

Adjust these JSON parameters:

* `model`: `gpt-image-1` (default).
* `prompt`: Text description.
* `n`: Number of images.
* `size`: `256x256`, `512x512`, or `1024x1024`.
* `response_format`: `"url"` (default) or `"b64_json"`.

```
{
  "model": "gpt-image-1",
  "prompt": "...",
  "n": 2,
  "size": "512x512",
  "response_format": "b64_json"
}Copy to clipboardErrorCopied
```

### [Simple image editing](#/llm-image-generation?id=simple-image-editing-1)

Use the Edits endpoint with an image and a mask:

```
curl https://api.openai.com/v1/images/edits \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-image-1",
    "image": "data:image/png;base64,<BASE64_IMAGE>",
    "mask": "data:image/png;base64,<BASE64_MASK>",
    "prompt": "Add a rainbow in the sky above the mountains",
    "n": 1,
    "size": "1024x1024"
  }'Copy to clipboardErrorCopied
```

([curl - What’s the correct URL to test OpenAI API? - Stack Overflow](https://stackoverflow.com/questions/75041247/whats-the-correct-url-to-test-openai-api))

### [Editing options](#/llm-image-generation?id=editing-options-1)

Editing requests accept:

* `image`: Original image (base64 or URL).
* `mask`: PNG mask for inpainting.
* `prompt`: Instruction for the edit.
* `n`, `size`, `response_format` as above.
* Optional `user` field for attribution.

### [Costs and optimization](#/llm-image-generation?id=costs-and-optimization-1)

GPT Image 1 pricing (per 1M tokens): text input $5, image input $10, image output $40. Rough per-image costs:

* Low quality: ~$0.02
* Medium quality: ~$0.07
* High quality: ~$0.19 ([OpenAI’s GPT-Image-1 API — Create Stunning Images for Your Apps!](https://medium.com/h7w/openais-gpt-image-1-api-create-stunning-images-for-your-apps-902c4f6745b1), [Usage of gpt-image-1 is priced per token, with … - Hacker News](https://news.ycombinator.com/item?id=43787769))

To optimize:

* Choose smaller sizes (`256x256`).
* Generate fewer images (`n:1`).
* Use `response_format:"url"` to reduce payload.
* Cache frequent prompts or images.

[Previous

LLM Agents](#/llm-agents)

[Next

LLM Speech](#/llm-speech)