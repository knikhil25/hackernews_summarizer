import ollama
import re

MODEL = "llama3.2:3b"

def generate_global_summary(articles_data):
    """
    Generates a structured global summary using Ollama.
    """
    # Prepare the context
    context = "You are a strict summarization engine. You must summarize the provided articles individually.\n"
    context += "Requirements:\n"
    context += "1. Process every single article provided below. Output them as a list of HTML blocks.\n"
    context += "2. SEPARATOR: Put exactly TWO newlines (\\n\\n) between each article summary.\n"
    context += "3. TITLE FORMAT: Start each article block with: <b><title></b><br>\n"
    context += "4. CONTENT: In the next line, write exactly ONE paragraph of summary text.\n"
    context += "5. FOOTER FORMAT: Append this HTML to the end of the text on the next line. IMPORTANT: include age like this: (inline): (Posted <age> ago) <a href=\"https://news.ycombinator.com/item?id=<id>\" target=\"_blank\">View on HN</a>\n"
    context += "6. CRITICAL: Do NOT use markdown (**bold**). Use HTML <b>bold</b> only. Do NOT bold the footer.\n"
    context += "7. Do not include any intro, outro, or headings like 'Global Tech Digest'.\n\n"
    context += "Articles:\n"
    
    valid_articles = 0
    for art in articles_data:
        title = art.get('title', 'Unknown')
        content = art.get('content', '')
        score = art.get('score', 0)
        age = art.get('age_text', 'recently')
        hn_id = art.get('id', '')
        
        # Skip if content is too short
        if len(content) < 100:
            continue
            
        # Truncate content to avoid blowing up context window (though 3.2 is good)
        # 1500 chars is usually enough for the core point
        truncated_content = content[:1500].replace('\n', ' ')
        
        context += f"--- ARTICLE: {title} (ID: {hn_id}, Score: {score}, Age: {age}) ---\n{truncated_content}\n\n"
        valid_articles += 1
        
    if valid_articles == 0:
        return "No valid content found to summarize."

    print(f"Sending {valid_articles} articles to Ollama ({MODEL})...")
    
    try:
        response = ollama.chat(model=MODEL, messages=[
            {
                'role': 'user',
                'content': context,
            },
        ])
        
        content = response['message']['content']
        
        # 1. Strip any markdown bold asterisks that the LLM might still output
        content = content.replace('**', '')

        # 2. Ensure footer connects to the paragraph (remove newlines before footer)
        content = re.sub(r'(\n|\r)+\s*\(Posted', ' (Posted', content)

        return content
        
    except Exception as e:
        print(f"Ollama Error: {e}")
        return f"Error creating summary with Ollama: {e}. Is Ollama running?"

# Shim for old function signature if needed, but we updated main.py
def generate_summary(text):
    return "Individual creation deprecated."
