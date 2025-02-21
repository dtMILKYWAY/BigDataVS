import csv
import random

from utils.getHomePageData import alladlist
from utils.getPublicData import *
import re
from datetime import datetime
def getHotWordDataPage():
    # 调用 getAlladlist 方法获取数据
    adlist = getAlladlist()
    # 提取索引为 6 的数据并过滤空值
    index_6_data = [row[6] for row in adlist if row[6]]
    # 统计每个唯一值出现的次数
    hot_word_count = {}
    for word in index_6_data:
        if word in hot_word_count:
            hot_word_count[word] += 1
        else:
            hot_word_count[word] = 1
    # 将统计结果转换为列表形式
    hot_word_list = [(word, count) for word, count in hot_word_count.items()]
    return hot_word_list
def getHostWordLen(hotWord):
    commentlist = getAlladlist()
    hotWordLen = []
    for i in commentlist:
        # 检查 i[4] 是否为 None
        if i[6] is not None and i[6].find(hotWord) != -1:
            hotWordLen.append(i)
    return hotWordLen
from datetime import datetime


def getHotDataEchartsData():
    time_ranges = [
        '公元前2000 - 1000',
        '公元前1000 - 0',
        '0 - 500',
        '500 - 1000',
        '1000 - 1500',
        '1500 - 2000',
        '不详'
    ]
    xData = time_ranges.copy()
    yData = [0] * len(time_ranges)

    for ad in alladlist:
        time_str = ad[3]
        if not time_str or time_str == '(Null)' or time_str.strip() == '':
            index = time_ranges.index('不详')
            yData[index] += 1
            continue

        num_start = num_end = None
        # 匹配公元前的情况
        bc_match = re.search(r'公元前\s*(\d+)\s*-\s*(\d+)|公元前\s*(\d+)', time_str)
        if bc_match:
            if bc_match.group(1) and bc_match.group(2):
                num_start = -int(bc_match.group(1))
                num_end = -int(bc_match.group(2))
            else:
                num_start = -int(bc_match.group(3))
        # 匹配公元的情况
        ad_match = re.search(r'公元\s*(\d+)\s*-\s*(\d+)|公元\s*(\d+)', time_str)
        if ad_match:
            if ad_match.group(1) and ad_match.group(2):
                num_start = int(ad_match.group(1))
                num_end = int(ad_match.group(2))
            else:
                num_start = int(ad_match.group(3))
        # 匹配纯数字的情况
        num_match = re.search(r'\d+', time_str)
        if num_match and not bc_match and not ad_match:
            num_start = int(num_match.group())

        if num_start is not None:
            if num_end is None:
                if num_start < -2000:
                    index = 0
                elif num_start < -1000:
                    index = 1
                elif num_start < 0:
                    index = 2
                elif num_start < 500:
                    index = 3
                elif num_start < 1000:
                    index = 4
                elif num_start < 1500:
                    index = 5
                else:
                    index = 5
            else:
                if num_end < -2000:
                    index = 0
                elif num_end < -1000:
                    index = 1
                elif num_end < 0:
                    index = 2
                elif num_end < 500:
                    index = 3
                elif num_end < 1000:
                    index = 4
                elif num_end < 1500:
                    index = 5
                else:
                    index = 5
            yData[index] += 1

    return xData, yData
def getTextureByType(hotWord):
    if hotWord is None:
        return '未知'
    all_adlist = getAlladlist()
    hot_word_list = getHotWordDataPage()
    target_hot_word_count = None
    for word, count in hot_word_list:
        if word == hotWord:
            target_hot_word_count = count
            break
    if target_hot_word_count is None:
        return '未知'
    filtered_adlist = [row for row in all_adlist if row[6] == hotWord]
    if not filtered_adlist:
        return '未知'
    random_id = random.choice([item[0] for item in filtered_adlist])
    for item in filtered_adlist:
        if item[0] == random_id:
            return item[5]


def getHotDataArticle(flag):
    if flag:
        tableListOld = getAlladlist()
        hostList = []
        for item in tableListOld:
            item = list(item)
            hotWord = item[6]
            if hotWord is None:
                continue
            texture = getTextureByType(hotWord)
            item.append(texture)
            hostList.append(item)
    else:
        hostList = getAlladlist()
    return hostList