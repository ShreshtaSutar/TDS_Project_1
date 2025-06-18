---
title: "Browser: DevTools"
original_url: "https://tds.s-anand.net/#/devtools?id=browser-devtools"
downloaded_at: "2025-06-12T14:51:18.535525"
---

[Browser: DevTools](#/devtools?id=browser-devtools)
---------------------------------------------------

[Chrome DevTools](https://developer.chrome.com/docs/devtools/overview/) is the de facto standard for web development and data analysis in the browser.
You’ll use this a lot when debugging and inspecting web pages.

Here are the key features you’ll use most:

1. **Elements Panel**

   * Inspect and modify HTML/CSS in real-time
   * Copy CSS selectors for web scraping
   * Debug layout issues with the Box Model

   ```
   // Copy selector in Console
   copy($0); // Copies selector of selected elementCopy to clipboardErrorCopied
   ```
2. **Console Panel**

   * JavaScript REPL environment
   * Log and debug data
   * Common console methods:

   ```
   console.table(data); // Display data in table format
   console.group("Name"); // Group related logs
   console.time("Label"); // Measure execution timeCopy to clipboardErrorCopied
   ```
3. **Network Panel**

   * Monitor API requests and responses
   * Simulate slow connections
   * Right-click on a request and select “Copy as fetch” to get the request.
4. **Essential Keyboard Shortcuts**

   * `Ctrl+Shift+I` (Windows) / `Cmd+Opt+I` (Mac): Open DevTools
   * `Ctrl+Shift+C`: Select element to inspect
   * `Ctrl+L`: Clear console
   * `$0`: Reference currently selected element
   * `$$('selector')`: Query selector all (returns array)

Videos from Chrome Developers (37 min total):

* [Fun & powerful: Intro to Chrome DevTools](https://youtu.be/t1c5tNPpXjs) (5 min)
* [Different ways to open Chrome DevTools](https://youtu.be/X65TAP8a530) (5 min)
* [Faster DevTools navigation with shortcuts and settings](https://youtu.be/xHusjrb_34A) (3 min)
* [How to log messages in the Console](https://youtu.be/76U0gtuV9AY) (6 min)
* [How to speed up your workflow with Console shortcuts](https://youtu.be/hdRDTj6ObiE) (6 min)
* [HTML vs DOM? Let’s debug them](https://youtu.be/J-02VNxE7lE) (5 min)
* [Caching demystified: Inspect, clear, and disable caches](https://youtu.be/mSMb-aH6sUw) (7 min)
* [Console message logging](https://youtu.be/76U0gtuV9AY) (6 min)
* [Console workflow shortcuts](https://youtu.be/hdRDTj6ObiE) (6 min)
* [HTML vs DOM debugging](https://youtu.be/J-02VNxE7lE) (5 min)
* [Cache inspection and management](https://youtu.be/mSMb-aH6sUw) (7 min)

[Previous

Unicode](#/unicode)

[Next

CSS Selectors](#/css-selectors)