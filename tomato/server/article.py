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
from tomato.server.category_relation import CategoryRelation

class ArticleService():
    def create(self, article: Article):
        """新增文章
        Args:
            article: class, 文章对象
        :return 
            返回dict
        """
        article.id = md5_id()
        with db.auto_commit():
            db.session.add(article)

        return {"id": article.id, "title": article.title}
    
    def show(self, id: str):
        """文章详情
        Args:
            id: string, 文章ID
        :return
            flag: True or False (Not found)
            data: dict or None
        """
        row = db.session.query(Article.id, Article.title, User.name, Article.content)\
                .filter(Article.author_id==User.id)\
                .filter(Article.id==id, Article.deleted_at==DELETED_AT)\
                .first()

        if row is None:
            return False, None
        
        """查询文章分类信息"""
        category_handler = CategoryRelation()
        cats = category_handler.getCategory(row[0])

        data = {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "content": row[3],
            "cats": cats
        }
        return True, data
    
    def update(self, id: str, kwargs: object):
        """编辑文章
        Args:
            id: string, 文章ID
            kwargs: object, 更新的属性
              :title:  string
              :status: int
        Return bool
        """
        row = Article.query.filter_by(id=id)
        if row is None:
            return False

        with db.auto_commit():
            row.update(kwargs)

        return  True
    
    def list(self, where: object, offset=0, limit=15):
        """查询列表
        Args:
            where: object, 查询对象
            offset: int, 分页
            limit:  int, 页长
        :return
            data: list, 文章列表
            count: int, 文章数量
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
            
        return data, count

    def destory(self, id: str) -> bool:
        """删除文章
        Args:
            id: string, 文章ID
        """
        row = Article.query.filter_by(id=id)
        
        if row is None:
            return False

        with db.auto_commit():
            row.update({"deleted_at": datetime.now()})

        return True

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