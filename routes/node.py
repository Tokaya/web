from models.node import Node
from models.user import User
from models.topic import Topic
from routes import *

# for decorators
from functools import wraps


main = Blueprint('node', __name__)

Model = Node

#
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

@main.route('/new_node')
def index():
    ms = Model.query.all()
    return render_template('node_index.html', node_list=ms)

@main.route('/show')
def node_show(id=4):
    u = current_user()
    if u is None:
        return redirect(url_for('user.login_view'))
    m = Model.query.get(id)
    ms = Node.query.order_by(Node.id.desc()).all()
    t = Topic.query.order_by(Topic.id.desc()).all()
    for i in t:
        i.avatar = i.get_avatar()
    return render_template('node.html', node=m, node_list=ms, topic=t, user=u)

@main.route('/add_topic')
# @admin_required
def add_topic():
    ms = Node.query.order_by(Node.id.desc()).all()
    print(ms)
    return render_template('topic_add.html', node_list=ms)

@main.route('/<int:id>')
def show(id):
    u = current_user()
    if u is None:
        return redirect(url_for('user.login_view'))
    m = Model.query.get(id)
    ms = Node.query.order_by(Node.id.desc()).all()
    t = Topic.query.order_by(Topic.id.desc()).all()
    for i in t:
        i.avatar = i.get_avatar()
    return render_template('node.html', node=m, node_list=ms, topic=t, user=u)


@main.route('/edit/<id>')
# @admin_required
def edit(id):
    t = Model.query.get(id)
    return render_template('node_edit.html', todo=t)


@main.route('/add', methods=['POST'])
# @admin_required
def add():
    form = request.form
    m = Model(form)
    m.save()
    return redirect(url_for('.index'))


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    t = Model.query.get(id)
    t.update(form)
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>')
# @admin_required
def delete(id):
    t = Model.query.get(id)
    t.delete()
    return redirect(url_for('.index'))
