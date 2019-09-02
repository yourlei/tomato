# coding: utf-8
# 建立文章与分类标签关系
from datetime import datetime
from tomato.database.model import db
from tomato.database.model import DATETIME_FORMAT
from tomato.database.model import Category
from tomato.database.model import Category_Relationship
from tomato.utils.errCode import ErrCode
from tomato.utils.utils import md5_id
from tomato.utils.utils import output_json

class CategoryRelation():
    def bindCategory(self, name: str, aid: str):
        """文章添加到某个分类
        Args:
            name: string, 分类名
            aid: string, 文章ID
        """
        category = Category.query.filter(Category.name==name).first()
    
        if category is None:
            row = Category(name=name)
            row.id = md5_id()
            cid = row.id
            with db.auto_commit():
                db.session.add(row)
        else:
            cid = category.id

        with db.auto_commit():
            # duplicate key update
            # 若已存在则更新, 否则插入
            date = datetime.now()
            sql = "insert into tomato_category_relationship(cid, aid) values('%s', '%s') \
                on duplicate key update updated_at = '%s';" % (cid, aid, date.strftime(DATETIME_FORMAT))
            db.engine.execute(sql)
        
        return output_json(code=0)

if __name__ == "__main__":
    from tomato.app import app
    handler = CategoryRelation()
    with app.app_context():
        handler.bindCategory("python", "046ca2d20970aba1")