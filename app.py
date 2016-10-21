from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import render_template
from models import db
from models.todo import Todo
from models.user import User
from models.node import Node
from models.topic import Topic
from models.weibo import Weibo
from models.blog import Blog
from routes.user import main as routes_user
from routes.todo import main as routes_todo
from routes.node import main as routes_node
from routes.topic import main as routes_topic
from routes.weibo import main as routes_weibo
from routes.blog import main as routes_blog


app = Flask(__name__)
db_path = 'todo.sqlite'
manager = Manager(app)


def register_routes(app):
    app.register_blueprint(routes_user)
    app.register_blueprint(routes_weibo, url_prefix='/weibo')
    app.register_blueprint(routes_blog, url_prefix='/blog')
    app.register_blueprint(routes_todo, url_prefix='/todo')
    app.register_blueprint(routes_node, url_prefix='/node')
    app.register_blueprint(routes_topic, url_prefix='/topic')


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    db.init_app(app)
    register_routes(app)


def configured_app():
    configure_app()
    return app

@app.errorhandler(404)
def error404(e):
    return render_template('404.html')


@manager.command
def server():
    print('server run')
    # app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()

# gunicorn -b '0.0.0.0:80' redischat:app
