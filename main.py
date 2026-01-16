from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
from scraper import scrape_hn, fetch_article_content
from filter import is_tech_article, rank_articles
from summarizer import generate_global_summary
import concurrent.futures

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Go to /static/index.html to use the app"})

@app.get("/api/scrape_and_summarize")
async def api_scrape_and_summar():
    print("Starting scrape...")
    
    # Scrape - Increase depth to find older articles
    all_articles = scrape_hn(days=15, max_pages=30) 
    print(f"Scraped {len(all_articles)} articles.")
    
    # Filter
    tech_articles = [a for a in all_articles if is_tech_article(a)]
    print(f"Filtered down to {len(tech_articles)} tech articles.")
    
    # Rank
    top_articles = rank_articles(tech_articles)[:10]
    print(f"Selecting top {len(top_articles)} for summarization.")
    
    articles_with_content = []
    
    def process_content_fetch(article):
        content = fetch_article_content(article['url'])
        article['content'] = content 
        return article

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_article = {executor.submit(process_content_fetch, art): art for art in top_articles}
        for future in concurrent.futures.as_completed(future_to_article):
            try:
                data = future.result()
                articles_with_content.append(data)
            except Exception as exc:
                print(f"Generated an exception: {exc}")
    
    # Re-sort
    articles_with_content = sorted(articles_with_content, key=lambda x: x['score'], reverse=True)
    
    # Generate Global Summary with Ollama
    global_digest = generate_global_summary(articles_with_content)
    
    response_payload = {
        "summary": global_digest,
        "articles": [
            {
                "id": a['id'],
                "title": a['title'],
                "url": a['url'],
                "score": a['score'],
                "age_text": a['age_text'],
                "date": a['date'].isoformat()
            }
            for a in articles_with_content
        ]
    }
    
    return response_payload

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
