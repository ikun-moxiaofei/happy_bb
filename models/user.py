# 创建用户ORM模型
from exts import db
from datetime import datetime
from enum import Enum
from shortuuid import uuid
from werkzeug.security import generate_password_hash, check_password_hash


# 存放权限类型的枚举
class PermissionEnum(Enum):
    BOARD = "板块"
    POST = "帖子"
    COMMENT = "评论"
    FRONT_USER = "前台用户"
    CMS_USER = "后台用户"

# 正经的许可（权限）ORM模型
class PermissionModel(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Enum(PermissionEnum),nullable=False,unique=True)

# 这段代码定义了一个名为 role_permission_table 的表，它是一个关联表，用于存储角色和权限之间的关系。
# 该表包含两个列：role_id 和 permission_id。这两个列都是整数类型，分别引用了 role 表和 permission 表中的 id 列。
# 这意味着每一行都表示一个角色和一个权限之间的关系。例如，如果一行中 role_id 为 1，permission_id 为 2，则表示角色 1 拥有权限 2。
# 这种表通常用于实现多对多关系。在这种情况下，它表示一个角色可以拥有多个权限，而一个权限也可以被多个角色拥有
role_permission_table = db.Table(
    "role_permission_table",
    db.Column("role_id",db.Integer,db.ForeignKey("role.id")),
    db.Column("permission_id",db.Integer,db.ForeignKey("permission.id"))
)

# 角色ORM模型
class RoleModel(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),nullable=False)
    desc = db.Column(db.String(200),nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 表示与该角色关联的权限。这是一个关系属性，它使用 db.relationship 函数定义。
    # 该函数接受三个参数：第一个参数指定关联的模型类（即 PermissionModel），
    # 第二个参数指定关联表（即 role_permission_table），第三个参数指定反向引用（即 roles）。
    # 这意味着可以通过访问 RoleModel.permissions 属性来获取与某个角色关联的所有权限，
    # 也可以通过访问 PermissionModel.roles 属性来获取拥有某个权限的所有角色。
    permissions = db.relationship("PermissionModel", secondary=role_permission_table, backref="roles")

# 用户模型
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(100), primary_key=True, default=uuid)
    username = db.Column(db.String(50), nullable=False,unique=True)
    _password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    avatar = db.Column(db.String(100))                                  # 头像
    signature = db.Column(db.String(100))                               # 签名
    join_time = db.Column(db.DateTime, default=datetime.now)
    is_staff = db.Column(db.Boolean,default=False)                      # 是否为员工
    is_active = db.Column(db.Boolean, default=True)                     # 用户是否可用

    # 外键
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))
    role = db.relationship("RoleModel",backref="users")

    # __init__ 方法是在创建 UserModel 类的实例时调用的构造函数。
    # *args 和 **kwargs 是 Python 中的特殊参数，允许你在调用函数时传递任意数量的位置参数和关键字参数。
    # 首先，它检查 kwargs 字典中是否存在 "password" 键。如果存在，它会使用该密码设置用户的密码属性，然后从 kwargs 中移除 "password" 键。
    # 接着，它调用父类的 __init__ 方法，以确保其他属性的初始化也会发生。
    def __init__(self,*args,**kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(UserModel,self).__init__(*args,**kwargs)

    # @property 装饰器用于将方法 password 转换为一个只读属性。这意味着你可以像访问属性一样访问 password 方法，而无需使用括号调用。
    # password 方法通过返回 self._password 来获取用户的密码哈希值。
    @property
    def password(self):
        return self._password

    # @password.setter 装饰器用于将方法 password 的 setter 方法，允许你设置用户密码时自动进行哈希值加密。
    # 当你设置密码时，setter 方法会将原始密码传递给 generate_password_hash 函数，以生成并存储密码的哈希值。
    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    # 这个方法用于检查用户提供的原始密码是否与存储在数据库中的哈希密码匹配。
    # 它使用 check_password_hash 函数来比较原始密码与哈希密码，然后返回比较结果。
    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result

    # 这个方法用于检查用户是否具有特定权限。
    # 它接收一个权限名称作为参数，然后检查该权限名称是否在用户的角色的权限列表中。
    def has_permission(self, permission):
        return permission in [permission.name for permission in self.role.permissions]

