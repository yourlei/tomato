# coding: utf-8
# 建立文章与分类标签关系
from datetime import datetime
from tomato.database.model import db
from tomato.database.model import DATETIME_FORMAT
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
        """
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
        
        return output_json(code=0)
    
    def unbindCategory(self, name, aid):
        """解绑文章与分类关系
        Args:
            name: string, 分类名
            aid: string, 文章ID
        """
        category = Category.query.filter(Category.name==name).first()
        # 更新绑定deleted_at字段值设为已删除
        with db.auto_commit(): 
            Category_Relationship.query\
                .filter(Category_Relationship.cid==category.id,
                Category_Relationship.aid==aid)\
                .update({"deleted_at": datetime.now()})

        return output_json(code=0)

if __name__ == "__main__":
    from tomato.app import app
    handler = CategoryRelation()
    with app.app_context():
        handler.unbindCategory("科学", "74d8ba70a83ac664")