from bottle import route, run, request, post, response
import pymysql.cursors

# Connect to the database in docker container
connection = pymysql.connect(host='db',
                             user='user',
                             password='password',
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)

# create tables if they don't exist
with connection:
    with connection.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS `article` (`id` int(11) NOT NULL AUTO_INCREMENT, `text` text NOT NULL, `url` varchar(255) NOT NULL, `political_bias` int(11) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;"
        cursor.execute(sql)
        sql = "CREATE TABLE IF NOT EXISTS `keywords` (`id` int(11) NOT NULL AUTO_INCREMENT, `keyword` varchar(255) NOT NULL, `article_id` int(11) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;"
        cursor.execute(sql)
    connection.commit()
        
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


# post article to database
@post('/article')
def article():
    id = None
    text = request.json.get('text')
    url = request.json.get('url')
    political_bias = request.json.get('political_bias')
    keywords = request.json.get('keywords')

    if not text or not url or not political_bias or not keywords:
        response.status = 500
        return {'status': 'error', 'message': 'missing data'}
    
    connection.ping() # reconnect if connection is closed, TODO: check if `with connection:` also reconnects
    
    with connection.cursor() as cursor:
        sql = "INSERT INTO `article` (`text`, `url`, `political_bias`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (text, url, political_bias))
        id = cursor.lastrowid
    with connection.cursor() as cursor:
        for keyword in keywords.split(','):
            sql = "INSERT INTO `keywords` (`keyword`, `article_id`) VALUES (%s, %s)"
            cursor.execute(sql, (keyword, id))
    connection.commit()
    return {'status': 'success', 'article_id': id}

run(host='0.0.0.0', port=8080, debug=True, reloader=True)
