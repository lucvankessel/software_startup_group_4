import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests

nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = SentimentIntensityAnalyzer()
thresholds = {'extreme_left': -0.5, 'moderately_left': -0.2, 'neutral_lower': -0.1, 'neutral_upper': 0.1,
              'moderately_right': 0.2, 'extreme_right': 0.5}


def get_dbpedia_annotations(text):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    data = {
        "text": text,
        "confidence": 0.5,
    }

    response = requests.post('http://dbpedia-spotlight/rest/annotate', headers=headers, data=data)

    if response.status_code == 200:
        json_response = response.json()
        return json_response.get('Resources', [])
    return []


def analyze_sentiment(text):
    return sentiment_analyzer.polarity_scores(text)['compound']


def get_opinion_orientation(sentence, entity):
    sentiment = analyze_sentiment(sentence.text)
    return sentiment


def classify_sentence(text, threshold=0.1):
    annotations = get_dbpedia_annotations(text)
    doc = nlp(text)
    total_sentiment = 0
    keywords = []

    for entity in annotations:
        entity_text = entity["@surfaceForm"]
        keywords.append(entity_text)
        sentence = next((sent for sent in doc.sents if entity_text in sent.text), None)
        if sentence:
            opinion_orientation = get_opinion_orientation(sentence, entity_text)
            total_sentiment += opinion_orientation

    return total_sentiment * 10, keywords

