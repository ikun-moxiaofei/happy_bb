from flask import Flask
import config
import hooks
from exts import db, mail, cache, csrf, avatars
from blueprints.cms import bp as cms_bp
from blueprints.user import bp as user_bp
from blueprints.front import bp as front_bp
from blueprints.post import bp as post_bp
from blueprints.media import bp as media_bp
from flask_migrate import Migrate
from models import user,post
import commands
from bbs_celery import make_celery

app = Flask(__name__)
# 连接数据库配置
app.config.from_object(config.DevelopmentConfig)
migrate = Migrate(app, db)

# 构建celery
celery = make_celery(app)

db.init_app(app)
mail.init_app(app)
cache.init_app(app)
avatars.init_app(app)

# CSRF保护
csrf.init_app(app)


# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)
app.register_blueprint(media_bp)

# 添加钩子函数
app.before_request(hooks.bbs_before_request)
app.errorhandler(401)(hooks.bbs_401_error)
app.errorhandler(404)(hooks.bbs_404_error)
app.errorhandler(500)(hooks.bbs_500_error)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

#添加命令
app.cli.command("create-permission")(commands.create_permission)
app.cli.command("create-role")(commands.create_role)
app.cli.command("create-test-user")(commands.create_test_user)
app.cli.command("create-admin")(commands.create_admin)
app.cli.command("create-board")(commands.create_board)
app.cli.command("create-test-post")(commands.create_test_post)

print(app.config.get("AVATARS_SAVE_PATH"))



if __name__ == '__main__':
        app.run(debug=True)