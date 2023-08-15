from flask import jsonify

# 这段代码定义了一组用于创建 RESTful 风格的 JSON 响应的辅助函数。
# 这些函数允许你根据不同的 HTTP 状态码和消息返回 JSON 格式的响应，
# 从而更容易在 Flask 应用中处理不同情况下的客户端请求。

class HttpCode(object):
  # 响应正常
  ok = 200
  # 没有登陆错误
  unloginerror = 401
  # 没有权限错误
  permissionerror = 403
  # 客户端参数错误
  paramserror = 400
  # 服务器错误
  servererror = 500


# 该函数用于返回 JSON 格式的响应。它接受三个参数：code（HTTP 状态码）、message（响应消息）和 data（响应数据）。
# 它会将这些参数组合成一个 JSON 对象并返回。
def _restful_result(code, message, data):
  return jsonify({"message": message or "", "data": data or {}}), code


def ok(message=None, data=None):
  return _restful_result(code=HttpCode.ok, message=message, data=data)


def unlogin_error(message="没有登录！"):
  return _restful_result(code=HttpCode.unloginerror, message=message, data=None)


def permission_error(message="没有权限访问！"):
  return _restful_result(code=HttpCode.paramserror, message=message, data=None)


def params_error(message="参数错误！"):
  return _restful_result(code=HttpCode.paramserror, message=message, data=None)


def server_error(message="服务器开小差啦！"):
  return _restful_result(code=HttpCode.servererror, message=message or '服务器内部错误', data=None)
