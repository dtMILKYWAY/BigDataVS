from utils.getPublicData import getAlladlist, getAllaflist
from datetime import datetime
alladlist = getAlladlist()
allaflist = getAllaflist()

def getHomePageData():
    # 作品的数量
    aflenmax = len(alladlist)
    # 最多数量的流派
    likecountmax = 0
    likecountmaxauthorname = ''
    # 最多作品类型
    typeDic = {}
    for ad in alladlist:
        if ad[8] is not None and likecountmax < int(ad[0]):
            likecountmax = int(ad[0])
            likecountmaxauthorname = ad[8]
        if typeDic.get(ad[5], -1) == -1:
            typeDic[ad[5]] = 1
        else:
            typeDic[ad[5]] += 1
    typeDicSorted = list(sorted(typeDic.items(), key=lambda x: x[1], reverse=True))
    return aflenmax, likecountmaxauthorname, typeDicSorted[0][0]

# getHomePageData.py 修改函数
def getHomeArtLikeCountTopFore():
    period_count = {}
    for ad in alladlist:
        period = ad[8]
        # 严格过滤空值、'(Null)' 和空白字符
        if period and str(period).strip() not in ['', '(Null)']:
            period = str(period).strip()  # 清理数据
            period_count[period] = period_count.get(period, 0) + 1
    sorted_periods = sorted(period_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_periods[:4]

import re


def getHomeartCreateChart():
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

def getHomeTypeChart():
    typesDic = {}
    for art in alladlist:
        if typesDic.get(art[6],-1) == -1:
            typesDic[art[6]] = 1
        else:
            typesDic[art[6]] += 1
    resultData = []
    for key,value in typesDic.items():
        resultData.append({
            'name':key,
            'value':value
        })
    return resultData

def getHomeInstutionEchart():
    InstutionDic = {}
    for art in alladlist:
        # 判断是否为空值
        if art[7] is None:
            key = "未知"
        else:
            key = art[7]
        if InstutionDic.get(key, -1) == -1:
            InstutionDic[key] = 1
        else:
            InstutionDic[key] += 1
    resultData = []
    for key, value in InstutionDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData

# getHomePageData.py 修改函数
def getHomeAuthorChart():
    author_count = {}
    for art in alladlist:
        author = art[4]  # 确保索引4对应作者字段
        if author and str(author).strip() not in ['', '(Null)']:
            author = str(author).strip()
            author_count[author] = author_count.get(author, 0) + 1
    # 按作品数量排序，取前10位避免数据过载
    sorted_authors = sorted(author_count.items(), key=lambda x: x[1], reverse=True)[:10]
    return [{"name": author, "value": count} for author, count in sorted_authors]