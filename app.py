from flask import Flask,render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:9tckay8Bv^9e@database-2.cfzewqbxonfb.us-east-2.rds.amazonaws.com:5432/postgres'
db = SQLAlchemy(app)
db.reflect()

# class tweetdb(db.Model):
#     __tablename__ = 'tweet'

# class sentiment(db.Model):
#     __tablename__ = 'sentiment'

# class user(db.Model):
#     __tablename__ = 'user'

@app.route("/")
def index():
    return render_template("index.html")

# Tweet Share
@app.route("/tweet_share")
def tweet_share():
    response = db.session.execute(
            "SELECT tweet.key_word, count(tweet.key_word) FROM tweet GROUP BY tweet.key_word").fetchall()
    tweets = []
    for i in response:
        dict = {}
        dict["total_count"] = i[1]
        dict["key_word"] = i[0]
        tweets.append(dict)
    return jsonify(tweets)

# Twitter Stacked
@app.route("/twitter_stacked")
def twitter_stacked():
    query = '''SELECT tweet.key_word
, SUM(CASE WHEN sentiment.mood < 0.3 THEN 1 ELSE 0 END) AS Negative
, SUM(CASE WHEN sentiment.mood > 0.7 THEN 1 ELSE 0 END) AS Positive
, SUM(CASE WHEN sentiment.mood > 0.3 AND sentiment.mood < 0.7 THEN 1 ELSE 0 END) AS Neutral
FROM tweet LEFT JOIN sentiment ON tweet.id = sentiment.id
GROUP BY  tweet.key_word'''
    response = db.session.execute(query).fetchall()
    tweets = []
    for i in response:
        dict = {}
        dict["key_word"] = i[0]
        dict["positive"] = i[2]
        dict["negative"] = i[1]
        dict["neutral"] = i[3]
        tweets.append(dict)
    return jsonify(tweets)

# NSAT
@app.route("/nsat")
def nsat():
    query = '''SELECT tweet.key_word, AVG( sentiment.mood)
FROM tweet LEFT JOIN sentiment ON tweet.id = sentiment.id
GROUP BY  tweet.key_word'''
    response = db.session.execute(query).fetchall()
    tweets = []
    for i in response:
        dict = {}
        dict["key_word"] = i[0]
        dict["nsat"] = i[1]
        tweets.append(dict)
    return jsonify(tweets)

# Time NSAT
@app.route("/time_nsat")
def nsat():
    query = '''pending'''
    response = db.session.execute(query).fetchall()
    tweets = []
    for i in response:
        dict = {}
        dict["key_word"] = i[0]
        dict["nsat"] = i[1]
        dict["year"] = i[1]  # From the date?
        tweets.append(dict)
    return jsonify(tweets)

# Tree Map
@app.route("/tree_map")
def nsat():
    query = '''pending'''
    response = db.session.execute(query).fetchall()
    tweets = []
    for i in response:
        dict = {}
        dict[""] = i[0]
        dict[""] = i[1]
        dict[""] = i[1]
        tweets.append(dict)
    return jsonify(tweets)

if __name__ == "__main__":
    app.run(debug=True)