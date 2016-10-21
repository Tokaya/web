from models.topic import Topic
from models.user import User
from models.topic import TopicComment
from routes import *


main = Blueprint('topic', __name__)

Model = Topic

def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u

@main.route('/')
def index():
    ms = Model.query.all()
    return render_template('topic_index.html', node_list=ms)


@main.route('/<int:id>')
def show(id):
    u = current_user()
    m = Model.query.get(id)
    ms = Topic.query.order_by(Topic.id.desc()).all()
    m.content = markdown(m.content)
    for i in ms:
        i.comment = i.load_comments()
        for o in i.comment:
            o.avatar = o.get_avatar()
        i.avatar = i.get_avatar()
        # print(i.comment)
    return render_template('topic.html', topic=m, user=u)


@main.route('/edit/<id>')
def edit(id):
    t = Model.query.get(id)
    return render_template('topic_edit.html', todo=t)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    if u is not None:
        form = request.form
        m = Model(form)
        m.node_id = int(form.get('node_id'))
        m.username = u.username
        m.user_id = u.id
        m.save()
        print("save", m.user_id)
        return redirect(url_for('node.show', id=m.node_id))
    else:
        abort(401)

@main.route('/comment', methods=['POST'])
def comment_add():
    u = current_user()
    if u is not None:
        print('comment_add', u.id, u.username)
        form = request.form
        c = TopicComment(form)
        c.user_id = u.id
        c.username = u.username
        c.topic_id = int(form.get('topic_id', -1))
        c.save()
        return redirect(url_for('.show', id=c.topic_id))
    else:
        abort(401)

@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    t = Model.query.get(id)
    t.update(form)
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>')
def delete(id):
    t = Model.query.get(id)
    t.delete()
    return redirect(url_for('.index'))
