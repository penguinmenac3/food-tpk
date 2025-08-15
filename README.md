
<div align="center">
 <h1>🍽️ Food Technologiepark Karlsruhe (TPK)</h1>
 <p>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python 3.12+"></a>
  <a href="#license"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
  <a href="#usage"><img src="https://img.shields.io/badge/CLI-Available-orange.svg" alt="CLI"></a>
 </p>
 <p>Get the weekly menu from Joel's Cantina at TPK, powered by AI & Vision! 🥗🤖</p>
</div>

## 🚀 Setup

1. **Install the package from source:**

 ```bash
 pip install -e .
 ```

2. **Configure environment variables** (`.env` supported):

 > **Note:** The model must be a VLM (vision capability), since the food is only provided as an image.

 ```bash
 export API_ENDPOINT="http://localhost:11434/v1"
 export API_KEY="ollama"
 export MODEL="gemma3:12b"
 ```

## 📦 Usage

Run the following commands to get the food menu for the current week, or to start the MCP server:

```bash
# Print in console
food-tpk

# Start MCP Server (stdio mode)
food-tpk-mcp

# Start MCP Server (http mode on port 13374)
food-tpk-mcp http
```

## 🛠️ How it works

1. 🔗 Download [`https://joels-cantina.de/blog/`](https://joels-cantina.de/blog/)
2. 🔍 Find all `<a>` tags containing href to `*tpk-speisekarte*.jpg`
3. 🗓️ Ask AI which of the filenames matches the current date (date and calendar week)
4. 🖼️ Download the image
5. 🤖 Give the image to AI and ask what is for food today (date) & ask for recommendation
6. 📦 Return result to user (including picture of speisekarte)

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

MIT
