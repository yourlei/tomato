# !/bin/bash
# 开发环境创建容器
sudo docker run -dti \
--name tomato \
-p 28095:8095 \
-v $PWD:/var/www/tomato \
-v /etc/localtime:/etc/localtime \
-w /var/www/tomato \
python:3.6-slim