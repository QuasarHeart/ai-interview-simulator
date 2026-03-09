from pymilvus import connections, utility

URI = "https://in03-c39e6c1284bf779.serverless.aws-eu-central-1.cloud.zilliz.com"
TOKEN = "1dec323ee439e13c775b6cfa6044d2bfe89e091827d64a01dc748855d4e031d1da71d8eb5955fdd44e660498f3c8d70c381aa210"

print("Connecting to:", URI)

connections.connect(
    alias="default",
    uri=URI,
    token=TOKEN,
)

print("Connected!")
print("Collections:", utility.list_collections())