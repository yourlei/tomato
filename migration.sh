#!/bin/bash
# 执行数据库结构迁移

db_dir="tomato/database"

if [ "$1"x = "first"x ]; then
  echo "初始化数据库..."
  cd ${db_dir}
  rm -r migrations 
  flask db init
  flask db migrate -m 'first'
  flask db upgrade
elif [ "$1"x = "upgrade"x ]; then
  echo "更新数据库表结构..."
  cd ${db_dir}
  flask db migrate
  flask db upgrade
else
  echo "Usage: 
    - ./migration.sh init,      首次初始化数据库
    - ./mirgration.sh upgrade,  更新数据表结构"
  exit
fi