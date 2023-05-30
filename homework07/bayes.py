# -*- coding: utf-8 -*-
import csv
import string
from collections import defaultdict
from math import *


class NaiveBayesClassifier:
    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.counters = defaultdict(lambda: defaultdict(int))
        self.uniq = set()
        self.class_counter = defaultdict(int)
        self.words_count = 0

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        for x, y in zip(X, y):
            self.class_counter[y] += 1
            for word in x.split():
                self.counters[y][word] += 1
                self.uniq.add(word)
                self.words_count += 1

    def predict(self, X):
        predicted = []
        total_documents = sum(self.class_counter.values())

        for string in X:
            class_scores = {}

            for class_i in self.counters:
                log_prior = log(self.class_counter[class_i] / total_documents)
                log_likelihood = 0

                for word in string.split():
                    count_of_curr_word_in_class = self.counters[class_i].get(word, 0)
                    count_of_words_in_curr_class = sum(self.counters[class_i].values())

                    log_likelihood += log(
                        (count_of_curr_word_in_class + self.alpha)
                        / (count_of_words_in_curr_class + self.alpha * len(self.uniq))
                    )

                class_scores[class_i] = log_prior + log_likelihood

            if not class_scores:
                raise Exception("Classifier is not fitted")

            predicted.append(max(class_scores, key=class_scores.get))

        return predicted

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        res = self.predict(X_test)
        c = 0
        for i in range(len(y_test)):
            if y_test[i] == res[i]:
                c += 1
        return c / len(y_test)


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


if __name__ == "__main__":
    with open("data/SMSSpamCollection", encoding="utf-8") as f:
        data = list(csv.reader(f, delimiter="\t"))
    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
    X = [clean(x).lower() for x in X]
    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
    model = NaiveBayesClassifier(1)
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
