from flask_mail import Message
from exts import mail
from celery import Celery

# send_mail 函数：这个函数用于发送邮件。它接受三个参数：recipient（收件人邮箱）、subject（邮件主题）和 body（邮件内容）。
# 在函数内部，它创建一个 Message 对象，然后使用 Flask-Mail 中的 mail.send 方法发送邮件。
def send_mail(recipient, subject, body):
    try:
        message = Message(subject=subject, recipients=[recipient], body=body)
        mail.send(message)
        print("邮件发送成功！")
    except Exception as e:
        print("邮件发送失败:", str(e))



# make_celery 函数：这个函数用于创建 Celery 对象，从而实现异步任务的处理。
# 它接受一个 app 参数，表示 Flask 应用实例。在函数内部，它通过 Celery 类来创建 Celery 对象，并配置后端和代理（broker）的设置
# 在make_celery函数中将send_mail添加到celery任务中
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    # 这是一个自定义的 Celery 任务基类，继承自 Celery 的默认任务类。
    # 它的目的是添加 Flask 应用的上下文到任务中，以确保任务在执行时可以访问应用的各种功能和扩展。
    TaskBase = celery.Task

    # 这是一个具体的任务类，继承自 TaskBase。它通过重写 __call__ 方法，在任务执行时激活 Flask 应用的上下文，然后再执行实际的任务。
    # 这样，任务在执行期间可以使用 Flask 的扩展、数据库连接等资源。
    class ContextTask(TaskBase):
        abstract = True
        # 这是在 ContextTask 类中定义的 __call__ 方法。当你调用一个 ContextTask 类的实例时，Python 解释器会自动执行这个方法。
        # 综合来说，def __call__(self, *args, **kwargs): 的作用是在任务执行时创建 Flask 应用上下文，
        # 然后再调用基类的 __call__ 方法来执行实际的任务逻辑。这样，任务在执行期间可以使用 Flask 的功能和扩展。
        def __call__(self, *args, **kwargs):
            # 这是上下文管理器，用于创建 Flask 应用上下文。在任务执行期间，这样可以确保任务可以访问 Flask 应用的功能和扩展。
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    # 将自定义的 ContextTask 类赋值给 Celery 实例的 Task 属性，从而确保所有的 Celery 任务都会使用这个具有 Flask 上下文的任务类。
    celery.Task = ContextTask
    # 将创建的 Celery 实例赋值给 Flask 应用实例的 celery 属性，以便在其他地方可以访问 Celery 实例。
    app.celery = celery

    # 添加任务
    # 注册 send_mail 函数为一个 Celery 任务。通过这个注册，send_mail 函数可以在应用中被异步调用。
    celery.task(name="send_mail")(send_mail)

    return celery