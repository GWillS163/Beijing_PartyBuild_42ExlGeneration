from gensim import corpora, models, similarities
import jieba
from collections import defaultdict

doc1 = 'E:/programCode/d1.txt'
doc2 = 'E:/programCode/d2.txt'
d1 = open(doc1).read()
d2 = open(doc2).read()
# 对文本进行分词
data1 = jieba.cut(d1)
data2 = jieba.cut(d2)
# 对分词的我文本整理成指定格式，"词语1  词语2  词语3...词语n"
data11 = ''
for item in data1:
    data11 += item + ' '

data21 = ''
for item in data2:
    data21 += item + ' '

# 存储文档到列表
documents = [data11, data21]
texts = [[word for word in document.split()]
         for document in documents]

# 计算词语的频率
frequency = defaultdict(int)  # 构建频率对象
for text in texts:
    for token in text:
        frequency[token] += 1
'''
#如果词汇量过多，去掉低频词
texts=[[word for word in text if frequency[token]>3]
 for text in texts]
'''
# 通过语料库建立词典
dictionary = corpora.Dictionary(texts)
dictionary.save('E:/programCode/wenben2.txt')
# 加载要对比文档
doc3 = 'E:/programCode/d3.txt'
d3 = open(doc3).read()
data3 = jieba.cut(d3)
data31 = ''
for item in data3:
    data31 += item + ' '
new_doc = data31
new_vec = dictionary.doc2bow(new_doc.split())  # 转换为稀疏矩阵
# 得到新的语料库
corpus = [dictionary.doc2bow(text) for text in texts]

ifidf = models.TfidfModel(corpus)
featureNUm = len(dictionary.token2id.keys())  # 得到特征数
index = similarities.SparseMatrixSimilarity(ifidf[corpus], num_features=featureNUm)
sim = index[ifidf[new_vec]]
print(sim)
#  Author : Github: @GWillS163
#  Time: $(Date)
