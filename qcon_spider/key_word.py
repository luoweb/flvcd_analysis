#!/usr/bin/python
# -*- coding: utf-8 -*-
# print 'test OK'
import sys
from nltk.tokenize import WordPunctTokenizer
import nltk
import jieba
from sklearn.feature_extraction.text import CountVectorizer
import scipy as sp

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt  
from wordcloud import WordCloud  

from collections import Counter

reload(sys)
sys.setdefaultencoding("utf-8")

tokenizer = WordPunctTokenizer()
summaryList = [];
file=open("./para.txt")
paras=file.readlines()
words=""
for para in paras:
    # print para
    seg_list = list(jieba.cut(para, cut_all=False))
    words +=" ".join(seg_list)
    summaryList.insert(0," ".join(seg_list))
#para='I like eat apple because apple is red but because I love fruit'
#统计词频
sentences = tokenizer.tokenize(words)#此处将para转为list
#print sentences
wordFreq=nltk.FreqDist(sentences)
print str(wordFreq.keys()).decode("unicode-escape")
#print dir(wordFreq)

print str(summaryList).decode("unicode-escape")
#转换为词袋
vectorizer = CountVectorizer(min_df=0,max_df=20)
#summaryList 是一个列表，每一个元素是一个句子 词与词之间使用空格分开，默认不会处理单个词（即一个汉字的就会忽略）
#可以通过修改vectorizer的正则表达式，解决不处理单个字的问题
#vectorizer.token_pattern='(?u)\\b\\w+\\b'
X = vectorizer.fit_transform(summaryList)
print str(vectorizer.get_feature_names()).decode("unicode-escape")
print X.shape
nums,features=X.shape   #帖子数量和词袋中的词数

#计算欧式距离
def dist_raw(v1,v2):
    delta=v1-v2
    return sp.linalg.norm(delta.toarray())

# #测试
# new_para='夏季新款清新碎花雪纺连衣裙，收腰显瘦设计；小V领、小碎花、荷叶袖、荷叶边的结合使得这款连衣裙更显精致，清新且显气质。'
# new_para_list=" ".join(list(jieba.cut(new_para, cut_all=False)))
# new_vec=vectorizer.transform([new_para_list])#new_para_list 是一个句子，词之间使用空格分开
# #print 'new_vec:',new_vec.toarray()

# minDis = 9999
# title=""
# for i in range(0,nums):
#     para = summaryList[i]
#     para_vec=X.getrow(i)
#     d=dist_raw(new_vec,para_vec)
#     #print X.getrow(i).toarray(),' = ',d
#     if(minDis > d):
#         minDis = d
#         title = para
# print title," = ",d
# print new_para_list
# print title



c = Counter()

for x in words:
    if len(x)>1 and x != '\r\n':
        c[x] += 1
print('常用词频度统计结果')
for (k,v) in c.most_common(100):
    print('%s%s %s  %d' % ('  '*(5-len(k)), k, '*'*int(v/3), v))

# wt = " /".join(mytext)  

file_handle=open('2018_qcon_keyword.txt',mode='w')
file_handle.write(words.encode('utf-8'))
file_handle.close()

#设置词云  
wc = WordCloud(background_color = "black", #设置背景颜色  
               max_words = 5000, #设置最大显示的字数  
               font_path = "simsun.ttf",  #设置中文字体，词云默认字体是“DroidSansMono.ttf字体库”，不支持中文 
               max_font_size = 50,  #设置字体最大值  
               random_state = 30, #设置有多少种随机生成状态，即有多少种配色方案  
    )  
mycloud= wc.generate(words)#生成词云  
  
#展示词云图  
plt.imshow(mycloud)  
plt.axis("off")  
plt.show() 


