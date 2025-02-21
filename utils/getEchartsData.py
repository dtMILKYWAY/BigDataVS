from utils import getPublicData
from collections import Counter
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image                   # 图片处理
import numpy as np

def getTypeList():
    all_ad_list = getPublicData.getAlladlist()
    filtered_list = [x for x in all_ad_list if all(x[i] for i in range(len(x)) if x[i] is not None)]
    typeList = list(set([x[5] for x in filtered_list]))
    return typeList


def getArticleCharOneData(defaultType):
    articleList = getPublicData.getAlladlist()
    # 过滤掉材质、类型等可能为空值的项
    filtered_article_list = [article for article in articleList if all(article[i] for i in [5, 6] if article[i] is not None)]
    unique_type_count = {}
    for article in filtered_article_list:
        if article[5] == defaultType:
            art_type = article[6]
            if art_type not in unique_type_count:
                unique_type_count[art_type] = 0
            unique_type_count[art_type] += 1
    xData = list(unique_type_count.keys())
    yData = list(unique_type_count.values())
    return xData, yData

def getArticleCharTwoData(defaultType):
    articleList = getPublicData.getAlladlist()
    # 过滤掉材质、博物馆等可能为空值的项
    filtered_article_list = [article for article in articleList if all(article[i] for i in [5, 7] if article[i] is not None)]
    unique_institution_count = {}
    for article in filtered_article_list:
        if article[5] == defaultType:
            institution = article[7]
            if institution not in unique_institution_count:
                unique_institution_count[institution] = 0
            unique_institution_count[institution] += 1
    xData = list(unique_institution_count.keys())
    yData = list(unique_institution_count.values())
    return xData, yData

def getArticleCharThreeData(defaultType):
    articleList = getPublicData.getAlladlist()
    # 过滤掉材质、创作时期等可能为空值的项
    filtered_article_list = [article for article in articleList if all(article[i] for i in [5, 8] if article[i] is not None)]
    unique_period_count = {}
    for article in filtered_article_list:
        if article[5] == defaultType:
            period = article[8]
            if period not in unique_period_count:
                unique_period_count[period] = 0
            unique_period_count[period] += 1
    xData = list(unique_period_count.keys())
    yData = list(unique_period_count.values())
    return xData, yData


from collections import Counter


def getTypeCharDataOne():
    all_data = getPublicData.getAlladlist()
    # 过滤掉作品类型为空值的项
    filtered_data = [x for x in all_data if x[6]]
    print("Filtered data:", filtered_data)  # 检查过滤后的数据

    # 正确统计每个类型的出现次数
    type_counter = Counter([x[6] for x in filtered_data])
    type_list = list(type_counter.keys())

    # 按出现次数降序排序
    sorted_types = sorted(type_counter.items(), key=lambda item: -item[1])

    xData = [t[0] for t in sorted_types]
    yData = [t[1] for t in sorted_types]

    bieData = [{"name": t, "value": c} for t, c in zip(xData, yData)]
    return xData, yData, bieData


def getTypeCharDataTwo():
    all_data = getPublicData.getAlladlist()
    # 过滤掉作品类型和作品材质为空值的项
    filtered_data = [x for x in all_data if x[6] and x[5]]

    # 初始化 bieData1 和 bieData2
    bieData1 = [{'name': '作品类型', 'value': 0}, {'name': '作品材质', 'value': 0}]
    bieData2 = [{'name': '作品类型', 'value': 0}, {'name': '作品材质', 'value': 0}]

    # 统计作品类型和作品材质的数量
    type_count = {}
    material_count = {}
    for item in filtered_data:
        art_type = item[6]
        material = item[5]

        # 统计作品类型
        if art_type not in type_count:
            type_count[art_type] = 1
        else:
            type_count[art_type] += 1

        # 统计作品材质
        if material not in material_count:
            material_count[material] = 1
        else:
            material_count[material] += 1

    # 将统计结果转换为 bieData1 和 bieData2 的格式
    bieData1 = [{'name': k, 'value': v} for k, v in type_count.items()]
    bieData2 = [{'name': k, 'value': v} for k, v in material_count.items()]

    return bieData1, bieData2


def getTypeCharDataThree():
    all_data = getPublicData.getAlladlist()
    # 过滤掉作品类型为空值的项
    filtered_data = [x for x in all_data if x[6]]
    type_count = {}
    for item in filtered_data:
        art_type = item[6]
        if art_type not in type_count:
            type_count[art_type] = 1
        else:
            type_count[art_type] += 1
    sorted_types = sorted(type_count.items(), key=lambda x: x[1], reverse=True)
    top_10_types = sorted_types[:10]
    x1Data = [t[0] for t in top_10_types]
    y1Data = [t[1] for t in top_10_types]
    return x1Data, y1Data