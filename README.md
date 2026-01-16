# Hacker News Ollama Summarizer

A web application that scrapes Hacker News for top tech articles from the last 15 days, filters and ranks them, and generates a concise, essay-style summary using a local Ollama LLM.

## Features

- **Smart Filtering**: Scrapes Hacker News and filters for genuine tech articles, excluding general news and controversy.
- **AI Summarization**: Uses a local Ollama model to generate a global summary of the top trends and stories.
- **Clean UI**: A modern, responsive web interface to view the summary and the list of top articles.
- **Recent Trends**: Focuses on the last 15 days to capture recent relevant discussions.

## Prerequisites

- **Python 3.8+**
- **Ollama**: You need to have [Ollama](https://ollama.com/) installed and running locally.
  - Pull a model (e.g., `llama3` or `mistral`): `ollama pull llama3`
  - Ensure the Ollama server is running.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/knikhil25/hackernews_summarizer.git
    cd hackernews_summarizer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the Ollama server** (if not already running):
    ```bash
    ollama serve
    ```

2.  **Run the application:**
    ```bash
    python main.py
    ```
    Alternatively, using uvicorn directly:
    ```bash
    uvicorn main:app --reload
    ```

3.  **Open the application:**
    Open your browser and navigate to: [http://localhost:8000/static/index.html](http://localhost:8000/static/index.html)

4.  **Generate Summary:**
    Click the "Generate Summary" button on the web page to start the scraping and summarization process.

## Project Structure

- `main.py`: FastAPI application entry point.
- `scraper.py`: Logic for scraping Hacker News and fetching article content.
- `filter.py`: Filtering and ranking logic for articles.
- `summarizer.py`: Interaction with Ollama for text summarization.
- `static/`: Frontend assets (HTML, CSS, JS).

## License

MIT
