import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, current_app
from flask_mail import Message
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from decorators import login_required
from exts import db, cache, mail
import random
from utils import restful
from forms.user import RegisterForm, LoginForm, EditProfileForm
from models.user import UserModel

# 和小傻子女朋友的互动
# import random小傻子你才是明明是你
# 是你就是你
# 哼
# from denglishu import sunruoxuan
# 小傻子

bp = Blueprint("user",__name__,url_prefix="/user")


# 邮箱验证
# 这里本来想用celety，但是一直报错就换成普通写法了
@bp.route("/mail/captcha")
def mail_captcha():
    try:
        email = request.args.get("mail")
        digits = ["0", "1", "2", "3", "4", "5"," 6", "7", "8", "9"]
        captcha = "".join(random.sample(digits,4))
        body = f"【happybb】您的验证码是：{captcha}"
        message = Message(subject="happybb",recipients=[email],body=body)
        mail.send(message)
        cache.set(email, captcha, timeout=100)
        return restful.ok()
    except Exception as e:
        print(e)
        return restful.server_error()

@bp.route("/register",methods=['GET','POST'])
def register():
  if request.method == 'GET':
    return render_template("front/register.html")
  else:
    form = RegisterForm(request.form)
    # 判断表单是否正确
    if form.validate():
      email = form.email.data
      username = form.username.data
      password = form.password.data
      user = UserModel(email=email,username=username,password=password)
      db.session.add(user)
      db.session.commit()
      return redirect(url_for("user.login"))
    else:
      for message in form.messages:
        flash(message)
      return redirect(url_for("user.register"))

@bp.route('/login',methods=['GET','POST'])
def login():
  if request.method == 'GET':
    return render_template("front/login.html")
  else:
    form = LoginForm(request.form)
    if form.validate():
      email = form.email.data
      password = form.password.data
      remember = form.remember.data
      user = UserModel.query.filter_by(email=email).first()
      if user and user.check_password(password):
        if not user.is_active:
          flash("该用户已被禁用！")
          return redirect(url_for("user.login"))
        session['user_id'] = user.id
        if remember:
          session.permanent = True
        return redirect("/")
      else:
        flash("邮箱或者密码错误！")
        return redirect(url_for("user.login"))
    else:
      for message in form.messages:
        flash(message)
      return render_template("front/login.html")

# 这是一个使用蓝图装饰器的视图函数定义，它表示当用户访问类似 /profile/<string:user_id> 的 URL 时，将执行下面的函数
@bp.get("/profile/<string:user_id>")
# 这个参数是通过 URL 提供的字符串值，用于标识要查看的用户的ID
def profile(user_id):
    # 行代码使用 SQLAlchemy 查询语句从数据库中获取指定 user_id 的用户对象。UserModel 应该是你的用户模型类。
    user = UserModel.query.get(user_id)
    is_mine = False
    # 这个条件语句检查是否存在名为 g.user 的变量（可能是通过用户登录信息存储在 g 对象中的），
    # 并且该用户的 ID 是否与当前访问的用户 ID 一致。
    # 这用于判断是否正在查看自己的个人资料。
    if hasattr(g,"user") and g.user.id == user_id:
        is_mine = True
    #  这是一个包含用户对象和是否是自己个人资料的布尔值的字典
    context = {
        "user": user,
        "is_mine": is_mine
    }
    print(user)
    return render_template("front/profile.html",**context)

@bp.post("/profile/edit")
@login_required
def edit_profile():
  form = EditProfileForm(CombinedMultiDict([request.form,request.files]))
  if form.validate():
    username = form.username.data
    avatar = form.avatar.data
    signature = form.signature.data

    # 如果上传了头像
    if avatar:
      # 生成安全的文件名
      filename = secure_filename(avatar.filename)
      # 拼接头像存储路径
      avatar_path = os.path.join(current_app.config.get("AVATARS_SAVE_PATH"), filename)
      # 保存文件
      avatar.save(avatar_path)
      # 设置头像的url
      g.user.avatar = url_for("media.media_file", filename="avatars/" + filename)

    g.user.username = username
    g.user.signature = signature
    db.session.commit()
    return redirect(url_for("user.profile",user_id=g.user.id))
  else:
    for message in form.messages:
      flash(message)
    return redirect(url_for("user.profile",user_id=g.user.id))

@bp.get('/logout')
def logout():
    session.clear()
    return redirect("/")

