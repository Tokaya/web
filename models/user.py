import hashlib
import os

from . import ModelMixin
from . import db
from . import timestamp



class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000))
    password = db.Column(db.String(1000))
    avatar = db.Column(db.String(1000))
    created_time = db.Column(db.Integer, default=0)


    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.avatar = form.get('avatar', 'http://icons.iconarchive.com/icons/ph03nyx/super-mario/256/Retro-Mario-icon.png')
        self.created_time = timestamp()

    def valid_login(self, u):
        return u.username == self.username and u.password == self.password

    def get_avatar(self):
        a = User.query.filter_by(username=self.username).first()
        if a is None:
            return 'http://icons.iconarchive.com/icons/ph03nyx/super-mario/256/Retro-Mario-icon.png'
        return a.avatar

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        else:
            return False

    def change_avatar(self, avatar):
        if len(avatar) > 2:
            self.avatar = avatar
            self.save()
            return True
        else:
            return False

    # 验证注册用户的合法性的
    def valid(self):
        valid_username = User.query.filter_by(username=self.username).first() == None
        valid_username_len = len(self.username) >= 3
        valid_password_len = len(self.password) >= 3
        # valid_captcha = self.captcha == '3'
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        elif not valid_username_len:
            message = '用户名长度必须大于等于 3'
            msgs.append(message)
        elif not valid_password_len:
            message = '密码长度必须大于等于 3'
            msgs.append(message)
        # elif not valid_captcha:
        #     message = '验证码必须输入 3'
        #     msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len
        return status, msgs
