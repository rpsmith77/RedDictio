from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_CONNECTION')
db = SQLAlchemy(app)
ma = Marshmallow(app)



# The Subreddits class is a table in the database that has four columns: subreddit_id, subreddit_name,
# hate_level, and last_edited
class Subreddits(db.Model):
    subreddit_id = db.Column(db.INTEGER, primary_key=True)  # Primary Key (Unique ID for db)
    subreddit_name = db.Column(db.TEXT, nullable=False)  # Text entered by user
    hate_level = db.Column(db.FLOAT, nullable=False)
    last_edited = db.Column(db.DATE)
    being_edited = db.Column(db.BOOLEAN)

    def __repr__(self):
        return '<%r>' % self.subreddit_id


# The Posts class is a model that will be used to create a table in the database. The table will have
# four columns: subreddit_id, post_id, post_title, and hate_level
class Posts(db.Model):
    subreddit_id = db.Column(db.INTEGER)
    post_id = db.Column(db.TEXT, primary_key=True)
    post_title = db.Column(db.TEXT)
    hate_level = db.Column(db.FLOAT)

    def __repr__(self):
        return '<%r>' % self.subreddit_id


# The class Comments is a table in the database with columns subreddit_id, post_id, comment_id,
# date_added, comment_text, and comment_hate
class Comments(db.Model):
    subreddit_id = db.Column(db.INTEGER)
    post_id = db.Column(db.TEXT)
    comment_id = db.Column(db.TEXT, primary_key=True)
    date_added = db.Column(db.DATE)
    comment_text = db.Column(db.TEXT)
    comment_hate = db.Column(db.FLOAT)

    def __repr__(self):
        return '<%r>' % self.subreddit_id


# This class is a subclass of the SQLAlchemyAutoSchema class, which is a subclass of the Marshmallow
# Schema class
class SubredditsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subreddits


class PostsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Posts


class CommentsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comments


# This is a query that is getting all of the subreddits from the database and ordering them by their
# name.
subreddits = Subreddits.query.order_by(Subreddits.subreddit_name).all()


@app.route('/', methods=['GET'])
@app.route('/index')  # multiple routes to same page
def home():
    """
    It returns the rendered template of the index.html file, and passes in the subreddits variable
    :return: The home function is returning the index.html file.
    """
    return render_template('index.html', subreddits=subreddits)


@app.route('/post/<subreddit_name>', methods=['GET'])
def subreddit_posts(subreddit_name):
    """
    "Return a rendered template of all posts in a subreddit, ordered by post title, where the hate level
    is not null."
    
    The first line of the function is a query to the Subreddits table to get the subreddit_id of the
    subreddit with the name passed in as an argument
    
    :param subreddit_name: The name of the subreddit you want to get posts from
    :return: A list of posts from a subreddit.
    """
    subreddit_id = Subreddits.query.filter(Subreddits.subreddit_name == subreddit_name).first().subreddit_id
    return render_template('subreddit_posts.html',
                           posts=Posts.query.order_by(Posts.post_title).filter(Posts.subreddit_id == subreddit_id,
                                                                               Posts.hate_level is not None),
                           subreddit_name=subreddit_name)


@app.route('/comment/<post_id>', methods=['GET'])
def subreddit_comments(post_id):
    """
    It renders the subreddit_comments.html template, passing in the comments for the post with the given
    post_id, and the title of the post
    
    :param post_id: The id of the post that we want to view the comments of
    :return: The subreddit_comments function is returning a render_template function.
    """
    post_title = Posts.query.filter(Posts.post_id == post_id).first().post_title
    return render_template('subreddit_comments.html',
                           comments=Comments.query.order_by(Comments.comment_id).filter(Comments.post_id == post_id),
                           post_title=post_title)


@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template('about_us.html')


@app.route('/api')
def api():
    """
    It takes the data from the database and returns it in a JSON format
    :return: A list of subreddits
    """
    subreddits_schema = SubredditsSchema(many=True)
    # too many comments to add to api
    # posts_schema = PostsSchema(many=True)
    # comments_schema = CommentsSchema(many=True)
    return jsonify({'Subreddits': subreddits_schema.dump(subreddits)})


@app.errorhandler(503)
def page_not_found(e):
    return render_template('503.html'), 503


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# This is a common pattern in Python. It is used to run the application when the file is run directly.
if __name__ == '__main__':
    app.run()
