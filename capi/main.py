from bottle import route, run, request, post, response, hook
import pymysql.cursors
from dotenv import load_dotenv
import os
import requests

load_dotenv()


# Connect to the database in docker container
def get_db_connection():
    return pymysql.connect(host=os.getenv("DATABASE_HOST", "db"),
                           user='user',
                           password='password',
                           database='db',
                           cursorclass=pymysql.cursors.DictCursor)


# CORS Handling
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        if request.method != 'OPTIONS':
            return fn(*args, **kwargs)

    return _enable_cors


@hook('after_request')
def after_request():
    response.headers['Access-Control-Allow-Origin'] = '*'


@route('/', method=['OPTIONS', 'GET'])
@enable_cors
def index():
    return {
        "French": "Salut, Monde!",
        "Spanish": "¡Hola, Mundo!",
        "Italian": "Ciao, Mondo!",
        "Japanese": "こんにちは、世界！",
        "German": "Hallo, Welt!",
        "Portuguese": "Olá, Mundo!",
        "Swedish": "Hej, Världen!",
        "Russian": "Привет, мир!",
        "Mandarin": "你好，世界！",
        "Arabic": "مرحبًا، عالم!",
        "Dutch": "Hallo, Wereld!",
        "Korean": "안녕하세요, 세계!",
        "Hindi": "नमस्ते, दुनिया!",
        "Greek": "Γεια σου, Κόσμε!",
        "Turkish": "Merhaba, Dünya!",
        "Swahili": "Habari, Dunia!",
        "Hebrew": "שלום, עולם!",
        "Thai": "สวัสดี, โลก!",
        "Vietnamese": "Chào, Thế giới!"
    }


@post('/article', method=['OPTIONS', 'POST'])
@enable_cors
def article():
    # see if the article is already in the database.
    # if not access the NLP/chatgpt to get the classification
    # send the article with classification to the RAD.
    # return the RAD results and the classification to the user.
    data = request.json
    if not data or 'url' not in data or 'text' not in data:
        response.status = 400  # Bad Request
        return {'status': 'error', 'message': 'Missing url or text in the request'}

    url = data['url']
    selected_text = data['text']

    # temporary only getting classification from NLP, TODO: integrate classification from chatGPT
    classification = get_classification(selected_text)
    if not classification:
        response.status = 500  # Internal Server Error
        return {'status': 'error', 'message': 'Error in classification'}

    keywords = ["Trump", "bad", "wall", "freedom", "tax"] # temporary assignment for testing, TODO: collect keywords according to selected_text

    rad_data = get_rad_data(selected_text, url, classification, keywords)
    if not rad_data:
        response.status = 500
        return {'status': 'error', 'message': 'Error in calling RAD service'}

    related_articles = rad_data['related_articles']

    return {'status': 'success', "classification": classification, "related_articles": related_articles}


# Helper Functions

def get_rad_data(text, url, political_bias, keywords):
    try:
        rad_payload = {
            'text': text,
            'url': url,
            'political_bias': political_bias,
            'keywords': ','.join(keywords)
        }
        rad_response = requests.post('http://rad:8080/article', json=rad_payload)
        rad_response.raise_for_status()  # This will raise an error for HTTP error codes
        return rad_response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error calling RAD service: {e}", flush=True)
        return None


def url_exists(url):
    query = "SELECT * FROM article WHERE url = %s"
    with get_db_connection().cursor() as cursor:
        cursor.execute(query, (url,))
        return cursor.fetchone() is not None


def get_classification(text):
    try:
        nlp_response = requests.post('http://nlp:8081/classify', json={'text': text})
        nlp_response.raise_for_status()
        return nlp_response.json().get('classification')
    except requests.exceptions.RequestException as e:
        print(f"Error calling NLP service: {e}", flush=True)
        return None


run(host='0.0.0.0', port=8082, debug=True, reloader=True)
