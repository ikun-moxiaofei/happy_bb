from flask import Blueprint, request, render_template, g, jsonify, redirect, url_for, current_app
from flask_paginate import Pagination

from exts import db
from forms.post import PublicPostForm
from models.post import BoardModel, PostModel
from decorators import login_required
from utils import restful

bp = Blueprint("post",__name__,url_prefix="/post")

@bp.route("/public",methods=['GET','POST'])
@login_required
def public_post():
    if request.method=='GET':
        boards = BoardModel.query.all()
        return render_template("front/public_post.html",boards=boards)
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            post = PostModel(title=title, content=content, board_id=board_id, author=g.user)
            db.session.add(post)
            db.session.commit()
            return restful.ok()
        else:
            message = form.messages[0]
            return restful.params_error(message=message)


# 这是一个使用蓝图装饰器的视图函数定义，它表示当用户访问 URL /post/detail/<int:post_id> 时，将执行下面的函数
@bp.get("/post/detail/<int:post_id>")
def post_detail(post_id):
    # 这行代码使用 SQLAlchemy 查询语句从数据库中获取指定 post_id 的帖子对象。
    post = PostModel.query.get(post_id)
    post.read_count += 1
    db.session.commit()

    is_mine = False
    # 这个条件语句检查是否存在名为 g.user 的变量（可能是通过用户登录信息存储在 g 对象中的），
    # 并且该用户的 ID 是否与当前访问的用户 ID 一致。
    # 这用于判断是否正在查看自己的个人资料。
    if hasattr(g, "user") and g.user.id == post.author_id:
        is_mine = True
    if hasattr(g, "user") and g.user.is_staff == True:
        is_mine = True


    return render_template("front/post_detail.html",post=post,is_mine=is_mine)


@bp.route("/delete_post/<int:post_id>", methods=['POST','GET'])
def delete_post(post_id):
    post = PostModel.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        # return redirect(url_for("front.index"))  # 重定向到首页

        boards = BoardModel.query.filter_by(is_active=True).all()

        # 获取页码参数
        page = request.args.get("page", type=int, default=1)
        # 获取板块参数
        board_id = request.args.get("board_id", type=int, default=0)

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
        pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2,
                                alignment="center")

        context = {
            "posts": posts,
            "boards": boards,
            "pagination": pagination,
            "current_board": board_id
        }
        current_app.logger.info("index页面被请求了")
        return render_template("front/index.html", **context)
    else:
        boards = BoardModel.query.filter_by(is_active=True).all()

        # 获取页码参数
        page = request.args.get("page", type=int, default=1)
        # 获取板块参数
        board_id = request.args.get("board_id", type=int, default=0)

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
        pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2,
                                alignment="center")

        context = {
            "posts": posts,
            "boards": boards,
            "pagination": pagination,
            "current_board": board_id
        }
        current_app.logger.info("index页面被请求了")
        return render_template("front/index.html", **context)