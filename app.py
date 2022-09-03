from flask import Flask, g, session
import config
from exts import db, mail
from blueprints import qa_bp, user_bp
from flask_migrate import Migrate
from model import UserModel

app = Flask(__name__)
# 加载config.py中的配置项
app.config.from_object(config)
# 加载数据库
db.init_app(app)
# 加载邮件服务
mail.init_app(app)
# 加载Migrate
migrate = Migrate(app, db)
# 注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)


@app.before_request
def before_request():
    '''
    钩子函数:每次发送请求前都会调用这个钩子函数
    '''
    uid = session.get("uid")
    if uid:
        user = UserModel.query.get(uid)
        # g为全局变量,参考js中的window
        g.user = user  # 等价于setattr(g,"user",user)


@app.context_processor
def context_processor():
    """
    上下文处理器，在执行完视图函数后，真正要返回内容前，执行上下文处理器函数
    """
    if hasattr(g, "user"):
        return {"user": g.user}
    return {}


if __name__ == '__main__':
    app.run()
