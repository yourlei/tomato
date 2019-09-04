# coding: utf-8
# 建立文章与分类标签关系
from datetime import datetime
from tomato.database.model import db
from tomato.database.model import DATETIME_FORMAT
from tomato.database.model import Article
from tomato.database.model import Category
from tomato.database.model import Category_Relationship
from tomato.utils.utils import md5_id
from tomato.utils.utils import output_json
from tomato.utils.errCode import ErrCode

class CategoryRelation():
    def bindCategory(self, name: str, aid: str):
        """文章添加到某个分类
        Args:
            name: string, 分类名
            aid: string, 文章ID
        :return
            False: 文章ID不存在
            True:　添加成功
        """
        # 文章是否存在
        article = Article.query.filter(Article.id==aid).first()

        if article is None:
            return False

        category = Category.query.filter(Category.name==name).first()
        # 分类不存在时,添加
        if category is None:
            row = Category(name=name)
            row.id = md5_id()
            cid = row.id
            with db.auto_commit():
                db.session.add(row)
        else:
            cid = category.id
        # 文章id与分类id绑定
        with db.auto_commit():
            # duplicate key update
            # 若已存在则更新, 否则插入
            date = datetime.now()
            sql = "insert into tomato_category_relationship(cid, aid) values('%s', '%s') \
                on duplicate key update updated_at = '%s';" % (cid, aid, date.strftime(DATETIME_FORMAT))
            db.engine.execute(sql)
        
        return True
    
    def unbindCategory(self, name: str, aid: str):
        """解绑文章与分类关系
        Args:
            name: string, 分类名
            aid: string, 文章ID
        :return 
            False: 分类不存在
            True: 解绑成功
        """
        category = Category.query.filter(Category.name==name).first()
        # 更新绑定deleted_at字段值设为已删除
        if category:
            with db.auto_commit(): 
                Category_Relationship.query\
                    .filter(Category_Relationship.cid==category.id,
                    Category_Relationship.aid==aid)\
                    .update({"deleted_at": datetime.now()})
        else:
            return False

        return True

    def getCategory(self, aid: str):
        """查询文章所属分类
        Args: 
            aid: string, 文章ID
        :return
            data: list, 分类列表
        """
        rows = Category_Relationship.query\
            .with_entities(Category_Relationship.cid)\
            .filter(Category_Relationship.aid==aid)\
            .all()
        
        data = []
        if len(rows):
            cat_ids = []
            for item in rows:
                cat_ids.append(item[0])

            res = db.session.query(Category.name)\
                .filter(Category.id.in_(cat_ids))\
                .all()
            for item in res:
                data.append(item[0])

        return data

if __name__ == "__main__":
    from tomato.app import app
    handler = CategoryRelation()
    with app.app_context():
        # handler.getCategory("74d8ba70a83c664")
        handler.unbindCategory("JS", 11)