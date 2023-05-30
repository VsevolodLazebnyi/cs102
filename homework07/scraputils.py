import requests  # type: ignore
from bs4 import BeautifulSoup
from db import News
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///news.db")
Session = sessionmaker(bind=engine)


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []
    items = parser.find("table", cellspacing="0", cellpadding="0", border="0")
    title = [a.text for a in items.select("span.titleline > a")]
    url = [a["href"] for a in items.select("span.titleline > a")]
    author = [a.text if a else "unknown" for a in items.select("span.subline > a.hnuser")]
    points = [s.text if s else 0 for s in items.select("span.score")]
    comments = [0 if "discuss" in c.text else c.text for c in items.select('span.subline > a[href^="item?id="]')]
    for i in range(len(title)):
        news_list.append(
            {"title": title[i], "url": url[i], "author": author[i], "points": points[i], "comments": comments[i]}
        )
    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    link = parser.find_all("a", class_="morelink")[0]["href"]
    return link


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    n = 1
    print("Collecting data from page: {}".format(url))
    while n_pages:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        session = Session()
        for item in news_list:
            news_item = News(
                title=item["title"],
                author=item["author"],
                url=item["url"],
                comments=item["comments"],
                points=item["points"],
            )
            session.add(news_item)
        session.commit()
        session.close()
        news.extend(news_list)
        n_pages -= 1
    return news
