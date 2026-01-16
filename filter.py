import re

# Positive keywords (Tech/Programming/Science focus)
TECH_KEYWORDS = [
    r'\bpython\b', r'\bjavascript\b', r'\brust\b', r'\bgo\b', r'\bgolang\b', r'\bc\+\+\b',
    r'\blinux\b', r'\bunix\b', r'\bmac\b', r'\bwindows\b', r'\bapi\b', r'\bdatabase\b',
    r'\bsql\b', r'\bnosql\b', r'\bserver\b', r'\bcloud\b', r'\baws\b', r'\bazure\b',
    r'\bgcp\b', r'\bdoocker\b', r'\bkubernetes\b', r'\bai\b', r'\bml\b', r'\bllm\b',
    r'\bmodel\b', r'\bneural\b', r'\balgorithm\b', r'\bcode\b', r'\bsoftware\b',
    r'\bdeveloper\b', r'\bdevops\b', r'\bgit\b', r'\bgithub\b', r'\bgitlab\b',
    r'\bweb\b', r'\bcss\b', r'\bhtml\b', r'\breact\b', r'\bvue\b', r'\bangular\b',
    r'\bnode\b', r'\bdeno\b', r'\bwasm\b', r'\bcompiler\b', r'\binterpreter\b',
    r'\bhacking\b', r'\bsecurity\b', r'\bvulnerability\b', r'\bexploit\b',
    r'\bcrypto\b', r'\bblockchain\b', r'\bbitcoin\b', r'\bethereum\b', r'\bdata\b',
    r'\banalytics\b', r'\bvisualization\b', r'\bperformance\b', r'\boptimization\b'
]

# Negative Keywords (Politics/Opinion/General News/Controversy)
NON_TECH_KEYWORDS = [
    r'\bpolitics\b', r'\btrump\b', r'\bbiden\b', r'\belection\b', r'\bvoting\b',
    r'\bgovernment\b', r'\blaw\b', r'\bcrime\b', r'\bmurder\b', r'\bkill\b',
    r'\bwar\b', r'\bpeace\b', r'\bisrael\b', r'\bpalestine\b', r'\brussia\b',
    r'\bukraine\b', r'\bchina\b', r'\busa\b', r'\bcongress\b', r'\bsenate\b',
    r'\bopinion\b', r'\beditorial\b', r'\binterview\b', r'\bhiring\b', r'\bjob\b', # "Who is hiring" are not articles
    r'\blaunch\b', # "Launch HN" are usually self-promo, technically tech but maybe not what user wants as "news"? Or keep? 
                   # User said "Plain news", usually "Launch HN" is tech product news. I'll keep Launch HN as it is tech.
                   # User said "should not controversy, opinions, only plain news". 
]

# Specifically strict negative list for pure controversy
CONTROVERSY_KEYWORDS = [
    r'\braped?\b', r'\bacused\b', r'\bsexual\b', r'\bassault\b', r'\bscandal\b',
    r'\blawsuit\b', r'\bsued\b', r'\bcourt\b', r'\bjudge\b'
]

def is_tech_article(article):
    """
    Heuristic to determine if an article is tech-focused and not controversy/politics.
    Checks title first (fast), then could check content (slow, so maybe avoid if possible).
    """
    title = article['title'].lower()
    
    # 1. Filter out controversy/politics strictly
    for kw in NON_TECH_KEYWORDS + CONTROVERSY_KEYWORDS:
        if re.search(kw, title):
            return False
            
    # 2. Check for Tech keywords
    # If it contains tech keywords, robustly accept it
    for kw in TECH_KEYWORDS:
        if re.search(kw, title):
            return True
            
    # 3. If no clear tech keyword, maybe it's still tech? 
    # For now, let's be strict to satisfy "Top 10 TECH articles". 
    # It's better to miss some than include non-tech.
    return False

def rank_articles(articles):
    """
    Ranks articles to get the top 10.
    Primary metric: Score (Points).
    Secondary metric: Recency (handled by filtering but maybe tie break).
    """
    # Simply sort by score descending
    sorted_articles = sorted(articles, key=lambda x: x['score'], reverse=True)
    return sorted_articles
