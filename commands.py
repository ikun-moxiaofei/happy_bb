# 命令
import random

import click
from faker import Faker

from models.post import BoardModel, PostModel
from models.user import PermissionModel,RoleModel,PermissionEnum,UserModel
from exts import db


def my_command():
    click.echo("这是我自定义的命令")

def create_permission():
    for permission_name in dir(PermissionEnum):
        if permission_name.startswith("__"):
            continue
        permission = PermissionModel(name=getattr(PermissionEnum,permission_name))
        db.session.add(permission)
    db.session.commit()
    click.echo("权限添加成功")

def create_role():
    # 审核
    inspector = RoleModel(name="审核",desc="审核帖子和评论")
    # 查询数据库以获取与指定权限名相匹配的权限对象，并将这些权限对象分配给inspector.permissions属性。
    # query 是一个用于构建数据库查询的方法，它允许你从数据库表中选择数据
    # filter 是用于添加过滤条件到查询中的方法，它用于缩小查询的结果集。你可以使用 filter 来添加多个过滤条件，使查询更加具体。
    inspector.permissions = PermissionModel.query.filter(PermissionModel.name.in_([
        PermissionEnum.POST,
        PermissionEnum.COMMENT
    ])).all()

    # 运营
    operator = RoleModel(name="运营",desc="负责网站正常运营")
    operator.permissions = PermissionModel.query.filter(PermissionModel.name.in_([
        PermissionEnum.POST,
        PermissionEnum.COMMENT,
        PermissionEnum.BOARD,
        PermissionEnum.FRONT_USER,
        PermissionEnum.CMS_USER
    ])).all()

    # 管理员
    adminitrator = RoleModel(name="管理员",desc="啥也负责")
    adminitrator.permissions = PermissionModel.query.all()

    db.session.add_all([inspector,operator,adminitrator])
    db.session.commit()
    click.echo("角色添加成功")


#创建测试员工账号
def create_test_user():
    admin_role = RoleModel.query.filter_by(name="管理员").first()
    zhangsan = UserModel(username="张三",email="zhangsan@qq.com",password="111111",is_staff=True,role=admin_role)

    operator_role = RoleModel.query.filter_by(name="运营").first()
    lisi = UserModel(username="李四", email="lisi@qq.com", password="111111", is_staff=True, role=operator_role)

    inspector_role = RoleModel.query.filter_by(name="审核").first()
    wangwu = UserModel(username="王五", email="wangwu@qq.com", password="111111", is_staff=True, role=inspector_role)

    db.session.add_all([zhangsan,lisi,wangwu])
    db.session.commit()
    click.echo("测试用户添加成功")


# 这个装饰器的作用是将指定的选项添加到命令行命令中，以便用户在命令行输入时可以提供相应的参数值。
# 当你在命令行中使用这些选项时，传递给选项的参数值会传递给被装饰的函数作为相应的参数。
@click.option("--username",'-u')
@click.option("--email",'-e')
@click.option("--password",'-p')
def create_admin(username,email,password):
  admin_role = RoleModel.query.filter_by(name="管理员").first()
  admin_user = UserModel(username=username, email=email, password=password, is_staff=True, role=admin_role)
  db.session.add(admin_user)
  db.session.commit()
  click.echo("管理员创建成功！")


def create_board():
    board_names = ['Python语法', 'web开发', '数据分析', '测试开发', '运维开发']
    for board_name in board_names:
        board = BoardModel(name=board_name)
        db.session.add(board)
    db.session.commit()
    click.echo("板块添加成功！")


def create_test_post():
  fake = Faker(locale="zh_CN")
  author = UserModel.query.first()
  boards = BoardModel.query.all()

  click.echo("开始生成测试帖子...")
  for x in range(98):
    title = fake.sentence()
    content = fake.paragraph(nb_sentences=10)
    random_index = random.randint(0,4)
    board = boards[random_index]
    post = PostModel(title=title, content=content, board=board, author=author)
    db.session.add(post)
  db.session.commit()
  click.echo("测试帖子生成成功！")