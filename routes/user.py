from models.user import User

from routes import *


# for decorators
from functools import wraps


main = Blueprint('user', __name__)

Model = User


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u

@main.route('/')
def home_page():
    return render_template('home.html')

@main.route('/index')
def index_page():
    u = User.query.order_by(User.id.desc()).all()
    for i in u:
        i.avatar = i.get_avatar()
    return render_template('index.html')

@main.route('/css_practice')
def css_practice():
    return render_template('css_practice.html')

@main.route('/login')
def login_view():
    u = current_user()
    if u is not None:
        return redirect('/index')
    return render_template('user_login.html')


@main.route('/user/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    if u.valid():
        u.save()
    else:
        abort(410)
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))


@main.route('/user/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    # 检查 u 是否存在于数据库中并且 密码用户 都验证合格
    user = User.query.filter_by(username=u.username).first()
    if user is not None and user.valid_login(u):
        print('登录成功')
        session['user_id'] = user.id
    else:
        print('登录失败')
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))


@main.route('/user/update_password', methods=['POST'])
def update_password():
    u = current_user()
    password = request.form.get('password', '')
    print('password', password)
    if u.change_password(password):
        print('修改成功')
    else:
        print('用户密码修改失败')
    return redirect('/profile')


@main.route('/user/update_avatar', methods=['POST'])
def update_avatar():
    u = current_user()
    avatar = request.form.get('avatar', '')
    print('password', avatar)
    if u.change_avatar(avatar):
        print('修改成功')
    else:
        print('用户密码修改失败')
    return redirect('/profile')


@main.route('/profile', methods=['GET'])
def profile():
    u = current_user()
    if u is not None:
        print('profile', u.id, u.username, u.password)
        return render_template('profile.html', user=u)
    else:
        return redirect(url_for('.login_view'))

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    print("注销", session)
    return redirect(url_for('.login_view'))