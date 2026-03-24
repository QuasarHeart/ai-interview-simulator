#! /bin/bash

set -e
VERSION=$1
REPO="ccr.ccs.tencentyun.com/fuchuang/java-app"

echo ">>> 拉取代码"
git pull origin Back-end-dev

echo "mvn 打包"
mvn clean package -DskipTests


docker build -t java-app:$VERSION .
docker tag java-app:$VERSION  $REPO:$VERSION
docker push $REPO:$VERSION
