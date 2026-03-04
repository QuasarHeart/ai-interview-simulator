"""version 1.0"""
"""确定一级维度里专业能力这一个维度的打分逻辑建模，确定以下四个二级维度的权重  
  1. 技术正确性
  2. 知识匹配度
  3. 岗位匹配度
  4. 工程实践能力
  使用TF-IDF（词频-逆文档频率）对99个后端岗位的招聘文本分析，
  并且进行可视化表示"""
import os
import re
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import matplotlib

# 1. 优先使用截图里显示的“Noto Sans CJK SC”或“WenQuanYi Micro Hei”
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'sans-serif']

# 2. 必须加上这一行，否则负号会显示为方块
plt.rcParams['axes.unicode_minus'] = False

#读取数据
def load_all_text(folder_path):
    all_text = ""
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                all_text += f.read() + "\n"
    return all_text

text = load_all_text("/home/yys/ai-interview-simulator/ml-service/data")  # 你的txt文件夹

#数据清洗
def clean_text(text):
    # 去数字+年以上
    text = re.sub(r"\d+年以上", "", text)
    text = re.sub(r"\d+年", "", text)
    
    # 去薪资
    text = re.sub(r"\d+k-\d+k", "", text, flags=re.IGNORECASE)
    
    # 去特殊符号
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z]", " ", text)
    
    return text

cleaned_text = clean_text(text)

# ===============================
# 按空行切分为单岗位 document
# ===============================

documents = re.split(r"\r?\n\s*\r?\n", text)

# 去掉太短的岗位
documents = [doc.strip() for doc in documents if len(doc.strip()) > 100]

print("总岗位数量：", len(documents))

stopwords = {
    "负责", "参与", "熟悉", "掌握", "具有", "相关",
    "协调", "组织", "开展", "实施", "推进", "协助",
    "对接", "完成", "处理", "执行", "从事","岗位职责",
    "精通", "了解", "熟练", "具备", "优秀", "良好",
    "一定", "专业", "以及", "及其", "对于", "关于",
    "各种", "多个", "一项", "一种", "基于", "通过",
    "进行", "提供", "经验", "能力", "项目",
    "工作", "要求", "目标", "内容", "日常", "事项",
    '以上','团队','优先', '使用','代码','能够','问题',
    '服务', '确保','以上学历','前端','学习','岗位','语言',
    '优先','能够','任职','问题','产品','确保','基础','理解','协作',
    '扎实','以上学历','公司','本科','规范','方案','独立','主流','学习','提升','质量',
    '合作','管理','语言','任务','岗位','精神','以上','交付','推动','建设',
    '深入','领域','复杂','常见','善于','快速','计算机相关','包括','其他','职位'
    }

# ===============================
# TF-IDF 建模
# ===============================

def chinese_tokenizer(text):
    words = jieba.lcut(text)
    words = [w for w in words if len(w) > 1 and w not in stopwords]
    return words

vectorizer = TfidfVectorizer(tokenizer=chinese_tokenizer)

X = vectorizer.fit_transform(documents)

feature_names = vectorizer.get_feature_names_out()

tfidf_sum = X.sum(axis=0)

word_scores = {
    feature_names[i]: tfidf_sum[0, i]
    for i in range(len(feature_names))
}

# 重新分词
#words = tokenize(cleaned_text)
#counter = Counter(words)

#print("Top 100 高频词：")
#print(counter.most_common(100))


# ===============================
# 定义 专业能力 二级维度关键词映射
# ===============================

ability_map = {

    # =====================================================
    # 一、技术正确性（底层理解 / 原理掌握 / 机制层）
    # =====================================================
    "算法": "技术正确性",
    "数据结构": "技术正确性",
    "时间复杂度": "技术正确性",
    "空间复杂度": "技术正确性",
    "原理": "技术正确性",
    "底层": "技术正确性",
    "机制": "技术正确性",
    "源码": "技术正确性",

    "并发": "技术正确性",
    "多线程": "技术正确性",
    "线程池": "技术正确性",
    "线程": "技术正确性",
    "锁": "技术正确性",
    "CAS": "技术正确性",
    "AQS": "技术正确性",
    "可见性": "技术正确性",
    "有序性": "技术正确性",
    "原子性": "技术正确性",

    "JVM": "技术正确性",
    "GC": "技术正确性",
    "类加载": "技术正确性",
    "内存模型": "技术正确性",
    "内存结构": "技术正确性",

    "事务": "技术正确性",
    "隔离级别": "技术正确性",
    "一致性": "技术正确性",
    "CAP": "技术正确性",
    "BASE": "技术正确性",

    "缓存击穿": "技术正确性",
    "缓存雪崩": "技术正确性",
    "缓存穿透": "技术正确性",


    # =====================================================
    # 二、知识匹配度（技术栈覆盖 / 工具掌握）
    # =====================================================
    "Java": "知识匹配度",
    "Spring": "知识匹配度",
    "SpringBoot": "知识匹配度",
    "SpringCloud": "知识匹配度",
    "MyBatis": "知识匹配度",
    "MySQL": "知识匹配度",
    "Redis": "知识匹配度",
    "MongoDB": "知识匹配度",

    "Kafka": "知识匹配度",
    "RocketMQ": "知识匹配度",
    "消息队列": "知识匹配度",

    "Nginx": "知识匹配度",
    "Docker": "知识匹配度",
    "Kubernetes": "知识匹配度",

    "Linux": "知识匹配度",
    "Git": "知识匹配度",
    "Maven": "知识匹配度",
    "Gradle": "知识匹配度",

    "HTTP": "知识匹配度",
    "HTTPS": "知识匹配度",
    "TCP": "知识匹配度",
    "IP": "知识匹配度",

    "数据库": "知识匹配度",
    "SQL": "知识匹配度",
    "索引": "知识匹配度",


    # =====================================================
    # 三、岗位匹配度（业务理解 / 场景落地）
    # =====================================================
    "业务": "岗位匹配度",
    "需求": "岗位匹配度",
    "场景": "岗位匹配度",
    "行业": "岗位匹配度",
    "产品": "岗位匹配度",
    "用户": "岗位匹配度",
    "客户": "岗位匹配度",

    "项目": "岗位匹配度",
    "解决方案": "岗位匹配度",
    "方案": "岗位匹配度",
    "流程": "岗位匹配度",
    "对接": "岗位匹配度",
    "交付": "岗位匹配度",

    "落地": "岗位匹配度",
    "转化": "岗位匹配度",
    "复盘": "岗位匹配度",


    # =====================================================
    # 四、工程实践能力（架构能力 / 工程规模能力）
    # =====================================================
    "架构": "工程实践能力",
    "架构设计": "工程实践能力",
    "系统设计": "工程实践能力",

    "分布式": "工程实践能力",
    "微服务": "工程实践能力",
    "服务治理": "工程实践能力",
    "注册中心": "工程实践能力",
    "限流": "工程实践能力",
    "熔断": "工程实践能力",
    "降级": "工程实践能力",

    "优化": "工程实践能力",
    "性能优化": "工程实践能力",
    "调优": "工程实践能力",

    "高并发": "工程实践能力",
    "高可用": "工程实践能力",
    "高性能": "工程实践能力",
    "容错": "工程实践能力",
    "扩展性": "工程实践能力",

    "重构": "工程实践能力",
    "代码规范": "工程实践能力",
    "代码质量": "工程实践能力",

    "测试": "工程实践能力",
    "单元测试": "工程实践能力",
    "自动化测试": "工程实践能力",

    "部署": "工程实践能力",
    "发布": "工程实践能力",
    "运维": "工程实践能力",
    "监控": "工程实践能力",

    "CI": "工程实践能力",
    "CD": "工程实践能力"
}

# ===============================
# 统计每个二级维度出现次数
# ===============================

#删除词频统计
#ability_counter = {}

#for word, count in counter.items():
#    if word in ability_map:
#        ability = ability_map[word]
#        ability_counter[ability] = ability_counter.get(ability, 0) + count

# ===============================
# 用 TF-IDF 聚合能力维度
# ===============================

ability_counter = {}

for word, score in word_scores.items():
    if word in ability_map:
        ability = ability_map[word]
        ability_counter[ability] = ability_counter.get(ability, 0) + score

print("\n各二级维度 TF-IDF 统计：")
print(ability_counter)


total = sum(ability_counter.values())
ability_weights = {}
if total == 0:
    print("没有匹配到能力关键词，请扩充 ability_map")
else:
    ability_weights = {
        ability: round(count / total, 3)
        for ability, count in ability_counter.items()
    }

    print("\n专业能力四个二级维度权重：")
    print(ability_weights)

matplotlib.use('Agg')
# 数据准备
labels = list(ability_weights.keys())
values = list(ability_weights.values())

# 创建图像
plt.figure(figsize=(8, 5))
plt.bar(labels, values)

# 标题和标签
plt.title("专业能力维度权重分布 (V1)")
plt.ylabel("Weight")
plt.xticks(rotation=45)

# 数值标注
for i, v in enumerate(values):
    plt.text(i, v + 0.01, f"{v:.2f}", ha='center')

# 保存图片
plt.tight_layout()
plt.savefig("ability_weight_v1.png")

#plt.show()