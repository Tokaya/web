from . import ModelMixin
from . import db
from . import timestamp
from . import blgtimestamp
from .user import User


class Blog(db.Model, ModelMixin):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000))
    created_time = db.Column(db.Integer)
    updated_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    content = db.Column(db.String(1000))
    title = db.Column(db.String(1000))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = blgtimestamp()
        self.username = form.get('username', '')
        self.comments = ''
        self.title = form.get('title', '')


    def update(self, form):
        self.content = form.get('content', '')
        self.save()

class BlogComment(db.Model, ModelMixin):
    __tablename__ = 'blogcomments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    created_time = db.Column(db.Integer, default=0)
    username = db.Column(db.String(1000))
    # 定义关系
    user_id = db.Column(db.Integer)
    weibo_id = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = timestamp()
        self.username = form.get('username', '')
        self.weibo_id = form.get('weibo_id', '')

    def get_avatar(self):
        a = User.query.filter_by(username=self.username).first()
        if a is None:
            return 'http://icons.iconarchive.com/icons/ph03nyx/super-mario/256/Retro-Mario-icon.png'
        return a.avatar
