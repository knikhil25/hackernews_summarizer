from summarizer import generate_global_summary
from datetime import datetime
import re

# Mock Data
mock_articles = [
    {
        "id": "12345",
        "title": "New Python Feature Released",
        "url": "https://python.org/new-feature",
        "score": 150,
        "age_text": "2 hours",
        "content": "Python has released a new feature that makes everything faster. " * 50
    },
    {
        "id": "67890",
        "title": "Ollama is Taking Over",
        "url": "https://ollama.com",
        "score": 200,
        "age_text": "5 hours",
        "content": "Ollama allows local LLM inference with ease. " * 50
    }
]

print("Running summarizer with mock data...")
summary = generate_global_summary(mock_articles)
print("\n--- GENERATED SUMMARY ---")
print(summary)
print("-------------------------")
