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

def scrape_hn(days=15, max_pages=25):
    """
    Scrapes Hacker News HTML and returns articles from the last `days`.
    Best-effort approach (HN pages are not strictly chronological).
    """
    cutoff = datetime.utcnow() - timedelta(days=days)
    articles = {}
    consecutive_old_pages = 0

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")

        try:
            r = requests.get(f"{HN_URL}news?p={page}", timeout=10)
            r.raise_for_status()
        except Exception as e:
            print(f"Request failed on page {page}: {e}")
            break

        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.select("tr.athing")

        if not rows:
            break

        page_has_recent = False

        for row in rows:
            try:
                story_id = row["id"]
                title_tag = row.select_one(".titleline > a")
                if not title_tag:
                    continue

                title = title_tag.get_text(strip=True)
                url = title_tag.get("href")
                if not url.startswith("http"):
                    url = urljoin(HN_URL, url)

                subtext = row.find_next_sibling("tr")
                if not subtext:
                    continue

                age_tag = subtext.select_one(".age > a")
                if not age_tag:
                    continue

                age_text = age_tag.get_text(strip=True)
                article_date = parse_relative_date(age_text)

                score_tag = subtext.select_one(".score")
                score = int(score_tag.get_text().split()[0]) if score_tag else 0

                articles[story_id] = {
                    "id": story_id,
                    "title": title,
                    "url": url,
                    "date": article_date,
                    "score": score,
                    "age_text": age_text,
                }

                if article_date >= cutoff:
                    page_has_recent = True

            except Exception as e:
                print(f"Parse error on page {page}: {e}")
                continue

        # Stop only after multiple pages with no recent articles
        if not page_has_recent:
            consecutive_old_pages += 1
        else:
            consecutive_old_pages = 0

        if consecutive_old_pages >= 3:
            print("No recent articles for several pages — stopping.")
            break

        time.sleep(0.25)

    return [a for a in articles.values() if a["date"] >= cutoff]

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
