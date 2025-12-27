import re

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return set(text.split())


def find_best_match(user_query, collection):
    user_words = preprocess(user_query)

    best_match = None
    best_score = 0

    for doc in collection.find():
        question_words = preprocess(doc["question"])

        common_words = user_words.intersection(question_words)
        score = len(common_words) / max(len(question_words), 1)

        if score > best_score:
            best_score = score
            best_match = doc

    return best_match, best_score
