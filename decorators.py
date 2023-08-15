from functools import wraps
from flask import redirect, url_for, g, abort, flash

# 定义了一个名为 login_required 的函数，这就是我们的装饰器。
# 装饰器函数接受一个参数 func，即将要被装饰的目标函数（视图函数）
def login_required(func):
  # 使用 @wraps(func) 装饰器，它能够确保被返回的内部函数（inner）保留被装饰函数的名称和文档字符串
  @wraps(func)
  def inner(*args, **kwargs):
    # 在 inner 函数内部，首先进行用户登录状态的检查。它通过检查全局变量 g 是否存在名为 "user" 的属性来判断用户是否已登录。
    # g 是 Flask 中的一个上下文全局变量，可以用于存储在请求生命周期内需要共享的数据。
    # hasattr(g, "user") 的作用是检查全局变量 g 是否具有名为 "user" 的属性。
    # 如果 g 中存在名为 "user" 的属性，那么表达式的值为 True，表示用户已登录；
    # 如果 g 中没有这个属性，表达式的值为 False，表示用户尚未登录
    if not hasattr(g, "user"):
      return redirect(url_for("user.login"))
    elif not g.user.is_active:
      flash("该用户已被禁用！")
      return redirect(url_for("user.login"))
    else:
      return func(*args, **kwargs)

  return inner


# 通过使用这个装饰器，你可以在需要进行权限控制的视图函数上方添加 @permission_required('some_permission') 这样的装饰器声明。
# 这将确保只有拥有特定权限的用户才能访问这些视图函数，否则会返回 403 错误。
# permission_required(permission) 是一个外部函数，接受一个参数 permission，表示所需的权限名称。它返回一个装饰器函数 outer。
def permission_required(permission):
  # outer(func) 是一个嵌套函数，接受一个参数 func，即要装饰的视图函数。它返回一个内部函数 inner。
  def outer(func):
    @wraps(func)
    # 是装饰器函数的内部实现。这个函数首先检查 g 上下文对象中是否存在 "user" 属性，并且该用户是否拥有传递给外部函数的 permission 权限
    def inner(*args, **kwargs):
      # 如果用户存在且拥有所需权限，那么 inner 调用原始的视图函数 func 并传递任何参数 args 和关键字参数 kwargs。
      # 这意味着只有在用户拥有权限时，才会执行原始的视图函数。
      if hasattr(g,"user") and g.user.has_permission(permission):
        return func(*args, **kwargs)
      else:
        # 如果用户不存在或者用户没有所需权限，inner 使用 abort(403) 来返回一个 HTTP 403 错误响应，表示禁止访问。
        # HTTP 403 错误通常表示服务器理解请求，但拒绝授权
        return abort(403)
    # 最后，inner 函数被返回，作为装饰器应用到原始的视图函数上
    return inner
  return outer