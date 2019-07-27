# !/bin/bash

sudo docker run -dti \
--name tomato \
-p 28095:8095 \
-v $PWD:/var/www/tomato \
-w /var/www/tomato \
python:3.6-slim