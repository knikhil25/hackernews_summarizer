import ollama
import re

MODEL = "llama3.2:3b"

def generate_global_summary(articles_data):
    """
    Generates a structured global summary using Ollama.
    """
    # Prepare the context
    context = "You are a Tech News Editor. Summarize the following top 10 articles into a cohesive Global Tech Digest.\n"
    context += "Requirements:\n"
    context += "1. Write in a clear, engaging essay style with distinct paragraphs.\n"
    context += "2. Each paragraph must be substantial, approximately 100 words long.\n"
    context += "3. START each paragraph with the Title of the main article, wrapped in <b> tags (e.g., <b>Title</b>: ...).\n"
    context += "4. Use <b> tags for emphasis where appropriate, instead of asterisks.\n"
    context += "5. Do NOT introduction or conclusion bloat. Jump straight into the news.\n"
    context += "6. Ignore any text that looks like navigation menus, pricing tables, or garbage.\n\n"
    context += "Articles:\n"
    
    valid_articles = 0
    for art in articles_data:
        title = art.get('title', 'Unknown')
        content = art.get('content', '')
        
        # Skip if content is too short
        if len(content) < 100:
            continue
            
        # Truncate content to avoid blowing up context window (though 3.2 is good)
        # 1500 chars is usually enough for the core point
        truncated_content = content[:1500].replace('\n', ' ')
        
        context += f"--- ARTICLE: {title} ---\n{truncated_content}\n\n"
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
        # Convert **text** to <b>text</b> just in case
        content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
        return content
        
    except Exception as e:
        print(f"Ollama Error: {e}")
        return f"Error creating summary with Ollama: {e}. Is Ollama running?"

# Shim for old function signature if needed, but we updated main.py
def generate_summary(text):
    return "Individual creation deprecated."
