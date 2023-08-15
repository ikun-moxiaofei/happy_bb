from exts import db
from datetime import datetime


# 板块模型
class BoardModel(db.Model):
  __tablename__ = 'board'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(20), nullable=False)
  create_time = db.Column(db.DateTime, default=datetime.now)
  # 它是一个布尔类型，表示板块是否激活。default=True 表示如果没有指定值，则默认为 True。
  is_active = db.Column(db.Boolean, default=True)


# 帖子模型
class PostModel(db.Model):
  __tablename__ = 'post'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(200), nullable=False)
  content = db.Column(db.Text, nullable=False)
  create_time = db.Column(db.DateTime, default=datetime.now)
  read_count = db.Column(db.Integer,default=0)
  is_active = db.Column(db.Boolean, default=True)
  # 这一行定义了一个名为 board_id 的列，它是一个整数类型，用于关联到板块的主键。
  # db.ForeignKey("board.id") 表示它是一个外键，指向 board 表格的 id 列。
  board_id = db.Column(db.Integer, db.ForeignKey("board.id"))
  author_id = db.Column(db.String(100), db.ForeignKey("user.id"), nullable=False)

  # 这一行定义了一个名为 board 的关系属性，它与 BoardModel 模型建立了一对多的关系。
  # backref="posts" 表示在 BoardModel 模型中可以通过 posts 来访问与该板块相关的所有帖子。
  board = db.relationship("BoardModel", backref="posts")
  author = db.relationship("UserModel", backref='posts')


# 评论模型
class CommentModel(db.Model):
  __tablename__ = 'comment'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  content = db.Column(db.Text, nullable=False)
  create_time = db.Column(db.DateTime, default=datetime.now)
  post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
  author_id = db.Column(db.String(100), db.ForeignKey("user.id"), nullable=False)
  is_active = db.Column(db.Boolean, default=True)

  post = db.relationship("PostModel", backref=db.backref('comments',order_by=create_time.desc()))
  author = db.relationship("UserModel", backref='comments')