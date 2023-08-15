import os
from flask import Blueprint, url_for, jsonify, current_app, request, render_template, flash, redirect, g
from flask_paginate import Pagination
from exts import db
from werkzeug.utils import secure_filename
from decorators import login_required
from exts import csrf
from forms.post import PublicCommentForm
from models.post import PostModel, BoardModel, CommentModel

bp = Blueprint("front",__name__,url_prefix="")

@bp.route("/")
def index():
  boards = BoardModel.query.filter_by(is_active=True).all()

  # 获取页码参数
  page = request.args.get("page", type=int, default=1)
  # 获取板块参数
  board_id = request.args.get("board_id",type=int,default=0)

  # 当前page下的起始位置
  start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")
  # 当前page下的结束位置
  end = start + current_app.config.get("PER_PAGE_COUNT")

  # 查询对象
  query_obj = PostModel.query.filter_by(is_active=True).order_by(PostModel.create_time.desc())
  # 过滤帖子
  if board_id:
    query_obj = query_obj.filter_by(board_id=board_id)
  # 总共有多少帖子
  total = query_obj.count()

  # 当前page下的帖子列表
  posts = query_obj.slice(start, end)

  # 分页对象
  pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

  context = {
    "posts": posts,
    "boards": boards,
    "pagination": pagination,
    "current_board": board_id
  }
  current_app.logger.info("index页面被请求了")
  return render_template("front/index.html", **context)

@bp.post("/upload/image")
@csrf.exempt
@login_required
def upload_image():
    f = request.files.get('image')
    extension = f.filename.split('.')[-1].lower()

    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return jsonify({
            "errno": 400,
            "data": []
        })

    filename = secure_filename(f.filename)
    file_path = os.path.join(current_app.config.get("UPLOAD_IMAGE_PATH"), filename)
    f.save(file_path)

    url = url_for('media.media_file', filename=filename)

    return jsonify({
        "errno": 0,
        "data": [{
            "url": url,
            "alt": "",
            "href": ""
        }]
    })

@bp.post("/post/<int:post_id>/comment")
@login_required
def public_comment(post_id):
  form = PublicCommentForm(request.form)
  if form.validate():
    content = form.content.data
    comment = CommentModel(content=content, post_id=post_id, author=g.user)
    db.session.add(comment)
    db.session.commit()
  else:
    for message in form.messages:
      flash(message)

  return redirect(url_for("post.post_detail", post_id=post_id))


from sqlalchemy import or_  # 导入 or_ 条件


@bp.route("/search")
def search():
    # 获取搜索关键字参数
    q = request.args.get("q")

    # 查询对象，过滤帖子并按创建时间降序排列
    query_obj = PostModel.query.filter_by(is_active=True).order_by(PostModel.create_time.desc())

    if q:
        # 如果有搜索关键字，使用 title 进行模糊搜索
        query_obj = query_obj.filter(PostModel.title.contains(q))

    # 获取分页参数
    page = request.args.get("page", type=int, default=1)
    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")
    end = start + current_app.config.get("PER_PAGE_COUNT")

    # 获取查询结果总数和当前页的帖子列表
    total = query_obj.count()
    posts = query_obj.slice(start, end)

    # 构建分页对象
    from flask_paginate import Pagination
    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

    boards = BoardModel.query.filter_by(is_active=True).all()
    board_id = request.args.get("board_id", type=int, default=0)
    if board_id:
        query_obj = query_obj.filter_by(board_id=board_id)
    context = {
        "posts": posts,
        "boards": boards,
        "pagination": pagination,
        "current_board": board_id
    }

    current_app.logger.info("search视图函数被请求了")
    return render_template("front/index.html", **context)