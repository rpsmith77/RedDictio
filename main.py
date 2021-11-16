"""
 Filler for testing
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///RedditDB.db'
db = SQLAlchemy(app)


class Subreddits(db.Model):
    """
        Tmp for nn
    """
    subreddit_id = db.Column(db.Integer, primary_key=True)  # Primary Key (Unique ID for db)
    subreddit_name = db.Column(db.TEXT, nullable=False)  # Text entered by user
    hate_level = db.Column(db.DECIMAL, nullable=False)
    last_edited = db.Column(db.DATE)  # Date and time entered
    being_edited = db.Column(db.BOOLEAN)

    def __repr__(self):
        return '<%r>' % self.subreddit_id


subreddit_scores = Subreddits.query.order_by(Subreddits.last_edited).all()


@app.route('/', methods=["GET"])
@app.route('/index')  # multiple routes to same page
def home():
    return render_template('index.html', subreddit_scores=subreddit_scores)


if __name__ == '__main__':
    app.run()
