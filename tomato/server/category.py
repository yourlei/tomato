# coding: utf-8
# 文章分类模块
from tomato.database.model import db
from tomato.database.model import Category
from tomato.utils.errCode import ErrCode
from tomato.utils.utils import md5_id
from tomato.utils.utils import output_json

class CategoryService():
    def create(self, name: str):
        """新增分类
        Args:
            name: string, 类名,值唯一
        """
        exist = Category.query.filter(Category.name==name).first()
        if exist:
            return output_json(code=ErrCode.EXIST_DATA)
        row = Category(name=name)
        row.id = md5_id()

        with db.auto_commit():
            db.session.add(row)

        return output_json(code=0)

    def update(self, id: str, kwargs: object):
        """更新分类
        Args:
            id: string,
            kwargs: object, 包含category属性的对象
        """
        exist = Category.query.filter_by(id=id)
        if exist is None:
            return output_json(code=ErrCode.NO_DATA)
        allow_field = ["name"]
        for key in kwargs.keys():
            if key not in allow_field:
                return output_json(code=ErrCode.ERR_PARAMS)
        if hasattr(kwargs, "name"):
            with db.auto_commit():
                exist.update(kwargs)

        return output_json(code=0)

    def list(self, where: object, offset=0, limit=15):
        """查询分类列表
        Args:
            where: object, 查询对象
            offset: int, 分页
            limit:  int, 页长
        """
        query = Category.query
        
        if where.get("name"):
            query = query.filter(Category.name==where.get("name"))
        
        count = query.count()
        rows = query.offset(offset).limit(limit).all()
        data = []
        for item in rows:
            data.append(item.to_dict())
        
        return output_json(data=data, total=count)

if __name__ == "__main__":
    from tomato.app import app
    with app.app_context():
        category = CategoryService()
        category.create("python")
        category.list({})