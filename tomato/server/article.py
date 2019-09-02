# coding: utf-8
# 文章管理模块
import traceback
from datetime import datetime
from tomato.setting import DBConfig
from tomato.database.model import db
from tomato.database.model import Article
from tomato.database.model import Category
from tomato.database.model import User
from tomato.utils.utils import md5_id
from tomato.utils.utils import DELETED_AT
from tomato.utils.utils import output_json
from tomato.utils.errCode import ErrCode

class ArticleService():
    def create(self, article: Article):
        """新增文章
        Args:
            article: class, 文章对象
        """
        # query = Article.query

        # exist = query.filter(Article.title==article.title, Article.author_id==
        #     article.author_id, Article.deleted_at==DELETED_AT)\
        #     .first()
        # if exist:
        #     return output_json(code=ErrCode.EXIST_DATA)

        article.id = md5_id()
        with db.auto_commit():
            db.session.add(article)

        return output_json(data={"id": article.id, "title": article.title}, code=0)
    
    def show(self, id: str):
        """文章详情
        Args:
            id: string, 文章ID
        """
        # row = Article.query().filter(Article.id==id, Article.deleted_at==DELETED_AT)\
        #     .first()

        row = db.session.query(Article.id, Article.title, User.name, Article.content)\
                .filter(Article.author_id==User.id)\
                .filter(Article.id==id, Article.deleted_at==DELETED_AT)\
                .first()

        if row is None:
            return output_json(code=ErrCode.NO_DATA)
        data = {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "content": row[3]
        }
        return output_json(data=data)
    
    def update(self, id: str, kwargs: object):
        """编辑文章
        Args:
            id: string, 文章ID
            kwargs: object, 更新的属性
              :title:  string
              :status: int
        """
        row = Article.query.filter_by(id=id)
        
        allowField = ["title", "status", "content"]
        # 检查更新字段
        for key in kwargs.keys():
            if key not in allowField:
                return output_json(code=ErrCode.ERR_PARAMS)
        if row is None:
            return output_json(code=ErrCode.NO_DATA)

        with db.auto_commit():
            row.update(kwargs)

        return  output_json(code=0)
    
    def list(self, where: object, offset=0, limit=15):
        """查询列表
        Args:
            where: object, 查询对象
            offset: int, 分页
            limit:  int, 页长
        """
        query = db.session.query(Article.id, Article.title, User.name,\
            Article.created_at)\
            .filter(Article.author_id==User.id)\
            .filter(Article.deleted_at==DELETED_AT)

        if where.get("title"):
            query = query.filter(Article.title.like("%" + where.get("title") + "%"))

        if where.get("author"):
            query = query.filter(User.name.like("%" + where.get("author") + "%"))

        count = query.count()
        rows = query.offset(offset).limit(limit).all()
        
        data = []
        for item in rows:
            data.append({
                "id": item[0],
                "title": item[1],
                "author": item[2],
                "created_at": item[3].strftime(DBConfig.DATETIME_FORMAT),
            })
            
        return output_json(data=data, code=0, total=count)

    def destory(self, id: str):
        """删除文章
        Args:
            id: string, 文章ID
        """
        row = Article.query.filter_by(id=id)
        
        if row is None:
            return output_json(code=ErrCode.NO_DATA)

        with db.auto_commit():
            row.update({"deleted_at": datetime.now()})

        return output_json(code=0)

if __name__ == "__main__":
    from tomato.app import app
    with app.app_context():
        article = ArticleService()
        # article.create(Article(
        #     title="linux防火墙",
        #     author="leiyu",
        #     content="kljsjdfjdkjdkj",
        #     cid="6c25cd76877c2"
        # ))
        res = article.list({})
        print(res)