from . import ModelMixin
from . import db
from . import timestamp
from .user import User


class Node(db.Model, ModelMixin):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    # has relationship with topic
    topics = db.relationship('Topic', backref="node")
    username = db.Column(db.String())

    def __init__(self, form):
        self.name = form.get('name', '')
        self.username = form.get('username', '')

    def get_avatar(self):
        a = User.query.filter_by(username=self.username).first()
        if a is None:
            return 'http://icons.iconarchive.com/icons/ph03nyx/super-mario/256/Retro-Mario-icon.png'
        return a.avatar
