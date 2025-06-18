---
title: "Static hosting: GitHub Pages"
original_url: "https://tds.s-anand.net/#/github-pages?id=static-hosting-github-pages"
downloaded_at: "2025-06-12T14:50:12.165587"
---

[Static hosting: GitHub Pages](#/github-pages?id=static-hosting-github-pages)
-----------------------------------------------------------------------------

[GitHub Pages](https://pages.github.com/) is a free hosting service that turns your GitHub repository directly into a static website whenever you push it. This is useful for sharing analysis results, data science portfolios, project documentation, and more.

Common Operations:

```
# Create a new GitHub repo
mkdir my-site
cd my-site
git init

# Add your static content
echo "<h1>My Site</h1>" > index.html

# Push to GitHub
git add .
git commit -m "feat(pages): initial commit"
git push origin main

# Enable GitHub Pages from the main branch on the repo settings pageCopy to clipboardErrorCopied
```

Best Practices:

1. **Keep it small**
   * [Optimize images](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/Multimedia). Prefer SVG over WEBP over 8-bit PNG.
   * [Preload](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel/preload) critical assets like stylesheets
   * Avoid committing large files like datasets, videos, etc. directly. Explore [Git LFS](https://git-lfs.github.com/) instead.

Tools:

* [GitHub Desktop](https://desktop.github.com/): GUI for Git operations
* [GitHub CLI](https://cli.github.com/): Command line interface
* [GitHub Actions](https://github.com/features/actions): Automation

[![Host a website using GitHub Pages](https://i.ytimg.com/vi_webp/WqOXxoGSpbs/sddefault.webp)](https://youtube.com/shorts/WqOXxoGSpbs)

[![Deploy your first GitHub Pages Website](https://i.ytimg.com/vi_webp/sT_zXIX3ZA0/sddefault.webp)](https://youtu.be/sT_zXIX3ZA0)

[Previous

Images: Compression](#/image-compression)

[Next

Notebooks: Google Colab](#/colab)