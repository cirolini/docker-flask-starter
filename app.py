from flask import Flask
from flaskext.mysql import MySQL
from redis import Redis, RedisError
from pymongo import MongoClient
import memcache
import os
import socket



MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "EXAMPLE")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "TEST")
MYSQL_USER = os.getenv("MYSQL_USER", "TEST")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "TEST")
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
MEMCACHE_HOST = os.getenv("MEMCACHE_HOST", "memcache")

app = Flask(__name__)

# Connect to Redis
redis = Redis(host=REDIS_HOST, db=0, socket_connect_timeout=2, socket_timeout=2)

# Connect to Memcache
mc = memcache.Client([MEMCACHE_HOST], debug=0)
mc.set("key", "1")

# Configure MySQL connection.
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = MYSQL_USER
app.config['MYSQL_DATABASE_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DATABASE_DB'] = MYSQL_DATABASE
app.config['MYSQL_DATABASE_HOST'] = MYSQL_HOST
mysql.init_app(app)

# Connect to mongodb
mongo = MongoClient(MONGO_HOST, 27017)
mongo_db = mongo.test

@app.route("/")
def hello():
    try:
        # try redis
        redis_result = redis.incr("counter")

        #try memcache
        memcache_result = mc.incr("key")

        #try mysql
        mysql_cursor = mysql.get_db().cursor()
        mysql_cursor.execute("SELECT * from test")
        mysql_result = mysql_cursor.fetchone()

        #try mongodb
        mongo_db.test.insert({"value": 1});
        mongo_result = mongo_db.test.find_one();
    except:
        print "ERROR"


    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Redis:</b> {redis_result}<br/>" \
           "<b>Memcache:</b> {memcache_result}<br/>" \
           "<b>Mysql:</b> {mysql_result}<br/>" \
           "<b>Mongodb:</b> {mongo_result}<br/>"

    return html.format(name=os.getenv("NAME", "world"), \
                       hostname=socket.gethostname(), \
                       redis_result=redis_result, \
                       memcache_result=memcache_result, \
                       mysql_result=mysql_result, \
                       mongo_result=mongo_result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
