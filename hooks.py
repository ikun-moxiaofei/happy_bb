# 钩子函数
from flask import session, g, render_template
from models.user import UserModel


def bbs_before_request():
    # 此行检查会话中是否存在密钥。如果是，则表示用户当前已登录。会话是存储在特定客户端的请求之间保留的数据的位置。
  if "user_id" in session:
    # 如果会话中存在该键，则此行将检索与其关联的值。此值可能表示当前经过身份验证的用户的 ID。
    user_id = session.get("user_id")
    try:
      # 在一个块内，此行查询数据库以查找与检索到的 .是表示用户信息的数据库模型
      # 如果从数据库中成功检索用户，则此行将用户对象存储在 Flask（全局）上下文中。
      # 上下文是一种存储数据的方法，可在请求的整个生命周期中访问。通过设置 ，可以使用户对象可用于正在处理当前请求的应用程序的其他部分。
      user = UserModel.query.get(user_id)
      setattr(g,"user",user)
    except Exception:
      pass


def bbs_404_error(error):
  return render_template("errors/404.html"), 404


def bbs_401_error(error):
  return render_template("errors/401.html"), 401


def bbs_500_error(error):
  return render_template("errors/500.html"), 500