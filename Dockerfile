FROM eclipse-temurin:25-jre-alpine

# 设置容器工作目录
WORKDIR /app

COPY target/*.jar app.jar

# 暴露端口
EXPOSE 8080

# 启动命令
ENTRYPOINT ["java", "-Dspring.output.ansi.enabled=ALWAYS", "-jar", "app.jar"]