---
title: "JavaScript tools: npx"
original_url: "https://tds.s-anand.net/#/npx?id=javascript-tools-npx"
downloaded_at: "2025-06-12T14:51:26.505575"
---

[JavaScript tools: npx](#/npx?id=javascript-tools-npx)
------------------------------------------------------

[npx](https://docs.npmjs.com/cli/v8/commands/npx) is a command-line tool that comes with npm (Node Package Manager) and allows you to execute npm package binaries and run one-off commands without installing them globally. It’s essential for modern JavaScript development and data science workflows.

For data scientists, npx is useful when:

* Running JavaScript-based data visualization tools
* Converting notebooks and documents
* Testing and formatting code
* Running development servers

Here are common npx commands:

```
# Run a package without installing
npx http-server .                # Start a local web server
npx prettier --write .           # Format code or docs
npx eslint .                     # Lint JavaScript
npx typescript-node script.ts    # Run TypeScript directly
npx esbuild app.js               # Bundle JavaScript
npx jsdoc .                      # Generate JavaScript docs

# Run specific versions
npx prettier@3.2 --write .        # Use prettier 3.2

# Execute remote scripts (use with caution!)
npx github:user/repo            # Run from GitHubCopy to clipboardErrorCopied
```

Watch this introduction to npx (6 min):

[![What you can do with npx (6 min)](https://i.ytimg.com/vi_webp/55WaAoZV_tQ/sddefault.webp)](https://youtu.be/55WaAoZV_tQ)

[Previous

Python tools: uv](#/uv)

[Next

Unicode](#/unicode)