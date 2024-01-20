from bottle import route, run, request, post, response, hook
import pymysql.cursors
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to the database in docker container
connection = pymysql.connect(host=os.getenv("DATABASE_HOST", "db"),
                             user='user',
                             password='password',
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)


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
    return {'status': 'success', "classification": "something", "related_articles": ["article 1", "article 2"]}


run(host='0.0.0.0', port=8082, debug=True, reloader=True)
