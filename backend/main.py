from bottle import route, run, request, post, response
import pymysql.cursors

# Connect to the database in docker container
connection = pymysql.connect(host='db',
                             user='user',
                             password='password',
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)


@route('/')
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

@post('/article')
def article():
    # see if the article is already in the database.
    # if not access the NLP/chatgpt to get the classification
    # send the article with classification to the RAD.
    # return the RAD results and the classification to the user.
    return {'status': 'success', "classification": "something", "related_articles": ["article 1", "article 2"]}

run(host='0.0.0.0', port=8081, debug=True, reloader=True)