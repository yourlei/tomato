# coding: utf-8
# 文章管理模块

import traceback
from datetime import datetime

from tomato.setting import DBConfig
from tomato.database.model import db
from tomato.database.model import Article
from tomato.database.model import Category
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
        query = Article.query

        exist = query.filter(Article.title==article.title, Article.author==
            article.author, Article.deleted_at==DELETED_AT)\
            .first()
        if exist:
            return output_json(code=ErrCode.EXIST_DATA)

        article.id = md5_id()
        db.session.add(article)
        db.session.commit()

        return output_json(code=0)
    
    def show(self, id: str):
        """文章详情
        Args:
            id: string, 文章ID
        """
        row = Article.query.filter(Article.id==id, Article.deleted_at==DELETED_AT)\
            .first()
        if row is None:
            return output_json(code=ErrCode.NO_DATA)
        
        return output_json(data=row.to_dict())
    
    def update(self, id: str, kwargs: object):
        """编辑文章
        Args:
            id: string, 文章ID
            kwargs: object, 更新的属性
              :title:  string
              :status: int
        """
        row = Article.query.filter_by(Article.id==id, Article.deleted_at==DELETED_AT)
        
        allowField = ["title", "status"]
        # 检查更新字段
        for key in kwargs.keys():
            if key not in allowField:
                return output_json(code=ErrCode.ERR_PARAMS)

        if row is None:
            return output_json(code=ErrCode.NO_DATA)
        try:
            row.update(kwargs)
            db.session.commit()
        except:
            print(traceback.format_exc())
            return output_json(code=ErrCode.SERVER_ERR)

        return  output_json(code=0)
    
    def list(self, where: object, offset=0, limit=15):
        """查询列表
        Args:
            where: object, 查询对象
            offset: int, 分页
            limit:  int, 页长
        """
        # query = Article.query
        query = db.session.query(Article.id, Article.title, Article.author,\
            Article.created_at)\
            .filter(Article.deleted_at==DELETED_AT)

        if where.get("title"):
            query = query.filter(Article.title.like("%" + where.get("title") + "%"))

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

        row.update({"deleted_at": datetime.now()})
        db.session.commit()

        return output_json(code=0)

if __name__ == "__main__":
    from tomato.app import app
    with app.app_context():
        article = ArticleService()
        article.create(Article(
            title="linux防火墙",
            author="leiyu",
            content="kljsjdfjdkjdkj",
            cid="6c25cd76877c2"
        ))
        article.list({})