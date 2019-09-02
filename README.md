### Tomato

 Flask开发的个人博客后台服务，系统前后端分离，该项目为后台接口服务

### 执行数据库迁移脚本

> 1. cd tomato/database

> 2. rm -r migrations

> 3. flask db init

> 4. flask db migrate -m 'first' (注意:*- m 'first' 首次初始化使用，后续更新不需要执行该步骤*)

> 5. flask db upgrade
