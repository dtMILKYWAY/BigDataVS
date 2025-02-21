from flask import Flask, session, render_template, redirect, Blueprint, request
from utils import getHotWordPageData, getHomePageData, getPublicData, getEchartsData
from snownlp import SnowNLP
from utils.getHomePageData import getHomePageData, getHomeTypeChart, getHomeInstutionEchart, getHomeAuthorChart
from utils.getHomePageData import getHomeArtLikeCountTopFore, getHomeartCreateChart
from utils.getHotWordPageData import getTextureByType
from utils.train_random_forest import getDataArticle

pb = Blueprint('page',__name__,url_prefix='/page',template_folder='templates')

@pb.route('/home')
def index():
    username=session.get('username')
    aflenmax, likecountmaxauthorname, typeMax=getHomePageData()
    ArtLikeCountTopFore=getHomeArtLikeCountTopFore()
    xData,yData=getHomeartCreateChart()
    typeChart=getHomeTypeChart()
    InstutionChart=getHomeInstutionEchart()
    AuthorChart=getHomeAuthorChart()
    return render_template('index.html',
                           username=username,
                           aflenmax=aflenmax,
                           likecountmaxauthorname=likecountmaxauthorname,
                           typeMax=typeMax,
                           ArtLikeCountTopFore=ArtLikeCountTopFore,
                           xData=xData,
                           yData=yData,
                           typeChart=typeChart,
                           InstutionChart=InstutionChart,
                           AuthorChart=AuthorChart
                            )


@pb.route('/hotWord')
def hotWord():
    username=session.get('username')
    hotWordlist=getHotWordPageData.getHotWordDataPage()
    defaultHotWord=hotWordlist[0][0]
    if request.args.get('hotWord'):defaultHotWord=request.args.get('hotWord')
    # 初始化默认热词的次数
    defaultHotWordNum = 0
    # 遍历热词列表，找到默认热词对应的次数
    for hotWord in hotWordlist:
        if defaultHotWord == hotWord[0]:
            defaultHotWordNum = hotWord[1]
            break
    tableList = getHotWordPageData.getHostWordLen(defaultHotWord)
    xData,yData = getHotWordPageData.getHotDataEchartsData()
    # 使用getHotDataArticle获取包含材质信息的列表
    flag = True
    hostList = getHotWordPageData.getHotDataArticle(flag)
    emotionValue = '未知'
    if hostList:
        for item in hostList:
            if item[6] == defaultHotWord:
                texture = getTextureByType(defaultHotWord)
                emotionValue = texture
                break

    return render_template('hotWord.html',
                           username=username,
                           hotWordlist=hotWordlist,
                           defaultHotWord=defaultHotWord,
                           defaultHotWordNum=defaultHotWordNum,
                           emotionValue=emotionValue,
                           tableList=tableList,
                           xData=xData,
                           yData=yData
                           )


@pb.route('/tableData')
def tableDataArticle():
    username = session.get('username')
    defaultFlag = False
    if request.args.get('flag'):
        defaultFlag = request.args.get('flag')
    tableData = getDataArticle(defaultFlag)
    return render_template('tableDataArt.html',
                           username=username,
                           defaultFlag=defaultFlag,
                           tableData=tableData
                           )

@pb.route('/artieChar')
def articleChar():
    username = session.get('username')
    typeList = getEchartsData.getTypeList()
    defaultType = typeList[0]
    if request.args.get('type'):
        defaultType = request.args.get('type')
    xData_type, yData_type = getEchartsData.getArticleCharOneData(defaultType)
    xData_institution, yData_institution = getEchartsData.getArticleCharTwoData(defaultType)
    xData_period, yData_period = getEchartsData.getArticleCharThreeData(defaultType)
    return render_template('artiChar.html',
                           username=username,
                           typeList=typeList,
                           defaultType=defaultType,
                           xData=xData_type,
                           yData=yData_type,
                           x1Data=xData_institution,
                           y1Data=yData_institution,
                           x2Data=xData_period,
                           y2Data=yData_period
                           )

@pb.route('/TypeChar')
def TypeChar():
    username = session.get('username')
    xData, yData, bieData = getEchartsData.getTypeCharDataOne()
    bieData1, bieData2 = getEchartsData.getTypeCharDataTwo()
    x1Data, y1Data = getEchartsData.getTypeCharDataThree()
    print("xData:", xData)  # 检查传递到模板的数据
    print("yData:", yData)
    print("bieData:", bieData)
    print("bieData1:", bieData1)
    print("bieData2:", bieData2)
    print("x1Data:", x1Data)
    print("y1Data:", y1Data)
    return render_template('TypeChar.html',
                           username=username,
                           xData=xData,
                           yData=yData,
                           bieData=bieData,
                           bieData1=bieData1,
                           bieData2=bieData2,
                           x1Data=x1Data,
                           y1Data=y1Data
                           )
