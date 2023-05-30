# -*- coding: utf-8 -*-
import random

from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import *


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    id = request.query.id

    s = session()
    news = s.query(News).filter(News.id == id).one()

    news.label = label
    s.commit()
    s.close()

    redirect("/news")


@route("/update")
def update_news():
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=1)
    s = session()
    existing_news = set((news.title, news.author) for news in s.query(News).all())
    news_to_add = []

    for news in news_list:
        if (news["title"], news["author"]) not in existing_news:
            news_to_add.append(
                News(
                    title=news["title"],
                    author=news["author"],
                    url=news["url"],
                    points=news["points"],
                    comments=news["comments"],
                )
            )

    s.add_all(news_to_add)
    s.commit()
    s.close()

    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    bayes = NaiveBayesClassifier()
    train = s.query(News).filter(News.label != None).all()
    x = [i.title for i in train]
    y = [i.label for i in train]
    bayes.fit(x, y)
    news = s.query(News).filter(News.label == None).all()
    X = [i.title for i in news]
    y = bayes.predict(X)
    for i in range(len(news)):
        news[i].label = y[i]
    s.commit()
    return sorted(news, key=lambda x: x.label)


@route("/recommendations")
def recommendations():
    classified_news = classify_news()
    return template("news_recommendations", rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
