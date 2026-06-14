"""数据库模型。

这个文件定义了数据库表的结构。
每个类对应数据库里的一张表。
"""

from sqlalchemy import Column, Integer, String
from app.database import Base


class Question(Base):
    """面试题目表。

    对应数据库里的 questions 表。
    """
    # 告诉 SQLAlchemy 这个模型对应哪张表
    __tablename__ = "questions"

    # id：主键，自动递增，唯一标识每道题目
    id = Column(Integer, primary_key=True, index=True)

    # title：题目标题，字符串，最多 200 个字符
    title = Column(String(200), nullable=False)

    # category：题目分类，字符串，最多 50 个字符
    category = Column(String(50), nullable=False)

    # difficulty：难度等级，整数，默认值 3
    difficulty = Column(Integer, default=3)
