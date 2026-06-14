"""数据库连接配置。

这个文件的作用：让 FastAPI 能连接到 SQLite 数据库。
SQLite 是一个轻量级数据库，数据会保存到一个 .db 文件里。
"""

# ========== 导入 SQLAlchemy 的工具 ==========

# create_engine：创建数据库"引擎"，相当于"数据库连接器"
from sqlalchemy import create_engine

# sessionmaker：创建"会话工厂"，每次操作数据库都需要一个会话
# DeclarativeBase：创建数据库模型的"基类"，所有模型都要继承它
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# ========== 数据库文件路径 ==========
# SQLite 会把数据存到这个文件里
# "./ai_interview.db" 表示当前目录下的 ai_interview.db 文件
# 如果文件不存在，SQLite 会自动创建
SQLALCHEMY_DATABASE_URL = "sqlite:///./ai_interview.db"


# ========== 创建数据库引擎 ==========
# engine 是"数据库连接器"，负责和数据库通信
# connect_args={"check_same_thread": False} 是 SQLite 特有的设置
# 原因：SQLite 默认只允许单线程访问，但 FastAPI 是多线程的
# 所以需要关闭这个检查，否则会报错
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# ========== 创建会话工厂 ==========
# SessionLocal 是一个"工厂"，每次调用它就会创建一个"会话"
# 会话（Session）是和数据库交互的"窗口"
# 就像打电话：Session 是电话，engine 是电话线，数据库是对方
SessionLocal = sessionmaker(
    autocommit=False,    # 不自动提交（需要手动 commit）
    autoflush=False,     # 不自动刷新（需要手动 flush）
    bind=engine          # 绑定到我们创建的引擎
)


# ========== 创建基类 ==========
# 所有数据库模型都要继承这个基类
# 就像所有"动物"都要继承"生物"这个类
class Base(DeclarativeBase):
    pass


# ========== 获取数据库会话的函数 ==========
# 这个函数会被 FastAPI 的 Depends 调用
# 作用：创建一个数据库会话，用完后自动关闭
def get_db():
    """获取数据库会话。

    使用方式：
        @app.get("/questions")
        def list_questions(db: Session = Depends(get_db)):
            # 用 db 操作数据库
            ...
    """
    # 创建一个会话
    db = SessionLocal()
    try:
        # yield 表示"暂停，把 db 交给调用者使用"
        # 调用者用完后，会继续执行下面的代码
        yield db
    finally:
        # 无论成功还是失败，最后都要关闭会话
        # 就像打完电话要挂掉
        db.close()
