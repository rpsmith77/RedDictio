"""
 Filler for testing
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Subreddit(db.Model):
    """
        Tmp for nn
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary Key (Unique ID for db)
    name = db.Column(db.String(200), nullable=False)  # Text entered by user
    score = db.Column(db.Float, nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)  # Date and time entered

    def __repr__(self):
        return '<%r>' % self.id


@app.route('/', methods=["GET"])
@app.route('/index')  # multiple routes to same page
def home():
    subreddit_scores = Subreddit.query.order_by(Subreddit.date_updated).all()
    return render_template('index.html', subreddit_scores=subreddit_scores)


if __name__ == '__main__':
    app.run()
