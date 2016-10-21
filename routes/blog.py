from models.blog import Blog
from models.user import User

from routes import *

# for decorators
from functools import wraps


main = Blueprint('blog', __name__)

Model = Blog


# def admin_required(f):
#     @wraps(f)
#     def function(*args, **kwargs):
#         # your code
#         print('admin required')
#         if request.args.get('uid') != '1':
#             print('not admin')
#             abort(404)
#         return f(*args, **kwargs)
#     return function

def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u

@main.route('/')
def index():
    u = current_user()
    if u is None:
        return redirect(url_for('user.login_view'))
    bl = Blog.query.order_by(Blog.id.desc()).all()
    for i in bl:
        i.content = markdown(i.content)
    return render_template('blog_index.html', blogs=bl, user=u)


@main.route('/<int:id>')
def show(id):
    m = Model.query.get(id)
    m.content = markdown(m.content)
    print(m.content)
    return render_template('blog.html', blog=m)


@main.route('/add_article')
# @admin_required
def add_article():
    return render_template('blog_add.html')


@main.route('/add', methods=['POST'])
# @admin_required
def add():
    u = current_user()
    if u is not None:
        print('blog add', u.id, u.username)
        form = request.form
        b = Blog(form)
        b.username = u.username
        b.user_id = u.id
        b.save()
        print(b, b.user_id, b.save())
        return redirect(url_for('.index'))
    else:
        abort(401)


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    t = Model.query.get(id)
    t.update(form)
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>')
# @admin_required
def delete(id):
    u = current_user()
    b = Model.query.get(id)
    if u.id == b.user_id:
        b.delete()
        return redirect(url_for('.index'))
    else:
        print('删除失败', u.id, b.user_id)
        return redirect(url_for('.index'))
