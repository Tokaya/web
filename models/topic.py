from . import ModelMixin
from . import db
from . import timestamp
from .user import User

class TopicComment(db.Model, ModelMixin):
    __tablename__ = 'topiccomments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=timestamp())
    updated_time = db.Column(db.Integer, default=timestamp())
    user_id = db.Column(db.Integer)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    username = db.Column(db.String())

    def __init__(self, form):
        print('comment init', form)
        self.content = form.get('content', '')
        self.created_time = timestamp()
        self.username = form.get('username', '')
        self.topic_id = form.get('topic_id', '')

    def get_avatar(self):
        a = User.query.filter_by(username=self.username).first()
        if a is None:
            return 'http://icons.iconarchive.com/icons/ph03nyx/super-mario/256/Retro-Mario-icon.png'
        return a.avatar

class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    user_id = db.Column(db.Integer)
    created_time = db.Column(db.Integer, default=timestamp())
    updated_time = db.Column(db.Integer, default=timestamp())
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    username = db.Column(db.String())

    def __init__(self, form):
        print('topic init', form)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.username = form.get('username', '')
        self.comments = ''

    def update(self, form):
        print('topic update', form)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.updated_time = timestamp()
        self.save()

    def get_avatar(self):
        a = User.query.filter_by(username=self.username).first()
        if a is None:
            return 'http://icons.iconarchive.com/icons/ph03nyx/super-mario/256/Retro-Mario-icon.png'
        return a.avatar

    def load_comments(self):
        cs = TopicComment.query.filter_by(topic_id=self.id).all()
        return cs