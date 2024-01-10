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
        sql = "CREATE TABLE IF NOT EXISTS `article` (`id` int(11) NOT NULL AUTO_INCREMENT, `text` text NOT NULL, `url` varchar(255) NOT NULL, `political_bias` int(11) NOT NULL, `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;"
        cursor.execute(sql)
        sql = "CREATE TABLE IF NOT EXISTS `keywords` (`id` int(11) NOT NULL AUTO_INCREMENT, `keyword` varchar(255) NOT NULL, `article_id` int(11) NOT NULL, PRIMARY KEY (`id`), FOREIGN KEY (`article_id`) REFERENCES `article`(`id`) ON DELETE CASCADE) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;"
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
    keywords = request.json.get('keywords', '').split(',')


    if not text or not url or not political_bias or not keywords:
        response.status = 500
        return {'status': 'error', 'message': 'missing data'}
    
    connection.ping() # reconnect if connection is closed, TODO: check if `with connection:` also reconnects
        
    articles = []

    # find related articles with the same keywords
    with connection.cursor() as cursor:
        # select from each political bias a few articles
        # range -100 to 100
        for bias in range(-100, 81, 20):
            sql = "SELECT id, url, political_bias, created_at FROM `article` WHERE `political_bias` BETWEEN %s AND %s AND `id` IN (SELECT `article_id` FROM `keywords` WHERE `keyword` IN (" + ("%s, " * len(keywords))[:-2] + "))"
            cursor.execute(sql, (bias, bias+19, *keywords))
            articles += [cursor.fetchall()]
        
        # sort by relevance for each political bias
        for bias_articles in articles:
            for article in bias_articles:
                article['relevance'] = len(set(keywords) & set(article['text'].split(' ')))
        
        for i in range(len(articles)):
            articles[i] = sorted(articles[i], key=lambda k: k['relevance'], reverse=True)[:3]
    
    with connection.cursor() as cursor:
        # insert article if it doesn't exist
        sql = "SELECT * FROM `article` WHERE `text`=%s AND `url`=%s AND `political_bias`=%s"
        cursor.execute(sql, (text, url, political_bias))
        article = cursor.fetchone()
        if not article:
            sql = "INSERT INTO `article` (`text`, `url`, `political_bias`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (text, url, political_bias))
        id = cursor.lastrowid if not article else article['id']

    with connection.cursor() as cursor:
        for keyword in keywords:
            sql = "INSERT INTO `keywords` (`keyword`, `article_id`) VALUES (%s, %s)"
            cursor.execute(sql, (keyword, id))
    connection.commit()
    # replace each article date with a string
    for i in range(len(articles)):
        for j in range(len(articles[i])):
            articles[i][j]['created_at'] = str(articles[i][j]['created_at'])
    return {'status': 'success', 'article_id': id, 'related_articles': articles}

run(host='0.0.0.0', port=8080, debug=True, reloader=True)
