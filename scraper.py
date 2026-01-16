import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import time
from urllib.parse import urljoin

HN_URL = "https://news.ycombinator.com/"

def parse_relative_date(date_str):
    """
    Parses HN relative dates like "2 hours ago", "1 day ago", "15 days ago".
    """
    now = datetime.now()
    if 'minute' in date_str:
        minutes = int(date_str.split()[0])
        return now - timedelta(minutes=minutes)
    elif 'hour' in date_str:
        hours = int(date_str.split()[0])
        return now - timedelta(hours=hours)
    elif 'day' in date_str:
        days = int(date_str.split()[0])
        return now - timedelta(days=days)
    else:
        return now

def scrape_hn(days=15, max_pages=15):
    """
    Scrapes HN for articles from the last `days`.
    """
    articles = []
    cutoff_date = datetime.now() - timedelta(days=days)
    current_page = 1
    
    while current_page <= max_pages:
        print(f"Scraping page {current_page}...")
        try:
            response = requests.get(f"{HN_URL}news?p={current_page}", timeout=10)
            if response.status_code != 200:
                break
            
            soup = BeautifulSoup(response.text, 'html.parser')
            athings = soup.find_all('tr', class_='athing')
            
            if not athings:
                break
                
            for athing in athings:
                try:
                    story_id = athing['id']
                    title_tag = athing.find('span', class_='titleline').find('a')
                    title = title_tag.text
                    url = title_tag['href']
                    
                    if not url.startswith('http'):
                        url = urljoin(HN_URL, url)
                    
                    subtext_row = athing.find_next_sibling('tr')
                    if not subtext_row:
                        continue
                        
                    age_span = subtext_row.find('span', class_='age')
                    if not age_span:
                         continue
                         
                    age_text = age_span.find('a').text
                    article_date = parse_relative_date(age_text)
                    
                    score_span = subtext_row.find('span', class_='score')
                    score = 0
                    if score_span:
                        score = int(score_span.text.split()[0])
                        
                    articles.append({
                        'id': story_id,
                        'title': title,
                        'url': url,
                        'date': article_date,
                        'score': score,
                        'age_text': age_text
                    })
                except:
                    continue
            
            # Stop if we are seeing old articles
            last_article = articles[-1] if articles else None
            if last_article and last_article['date'] < cutoff_date - timedelta(days=1):
                 print("Reached articles older than limit.")
                 break

            current_page += 1
            time.sleep(0.2) 
            
        except Exception as e:
            print(f"Error fetching page {current_page}: {e}")
            break
            
    final_articles = [a for a in articles if a['date'] >= cutoff_date]
    return final_articles

def fetch_article_content(url):
    """
    Fetches the textual content of an article using BeautifulSoup.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return ""
            
        soup = BeautifulSoup(response.text, 'lxml') 
        
        # Aggressive stripping
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "iframe", "noscript"]):
            tag.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        # Collapse spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
        
    except Exception as e:
        print(f"Failed to fetch content for {url}: {e}")
        return ""
