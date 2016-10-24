from . import ModelMixin
from . import db
from . import timestamp
from .user import User


class Weibo(db.Model, ModelMixin):
    __tablename__ = 'weibos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    created_time = db.Column(db.Integer, default=0)
    # 定义关系
    username = db.Column(db.String(1000))
    user_id = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = timestamp()
        self.username = form.get('username', '')
        self.comments = ''

    def load_comments(self):
        cs = Comment.query.filter_by(weibo_id=self.id).all()
        return cs

    def valid(self):
        return len(self.weibo) > 0 and len(self.weibo) < 140 and len(self.name) > 0

    def get_avatar(self):
        a = User.query.filter_by(username=self.username).first()
        if a is None:
            return 'http://icons.iconarchive.com/icons/ph03nyx/super-mario/256/Retro-Mario-icon.png'
        return a.avatar


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
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

    def json(self):
        d = {
            'id': self.id,
            'content': self.content,
            'created_time': self.created_time,
            'weibo_id': self.weibo_id,
            'user_id': self.user_id,
        }
        return json.dumps(d, ensure_ascii=False)
