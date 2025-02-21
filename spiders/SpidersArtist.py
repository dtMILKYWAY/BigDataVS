import requests
from lxml import etree


a=30
for b in range(1,a+1):
    url='https://www.artlib.cn/artist_list?page={}'.format(b)
    # #手动登录后，f12拿到cookie值
    params = {
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "cookie": "gfsessionid=14rojtr1og7clwd6n5uxv86kyqhoex2l"

    }

    # 发送GET请求获取网页内容
    response = requests.session()
    response=response.get(url,headers=params)
    # print(response)
    # 设置响应的编码为合理的编码格式，避免乱码问题
    response.encoding = response.apparent_encoding

    # 使用lxml的etree解析网页内容，得到一个可以使用xpath的对象
    dhtml = etree.HTML(response.text)

    #获取这一页有多少个艺术家
    div_count = len(dhtml.xpath('//div[@class="data-list"]/div'))

    for i in range(div_count):
        #得到网页地址
        id_value= dhtml.xpath('//div[@class="data-list"]/div/@onclick')[i]
        start_index = id_value.find('id=') + 3  # 找到id=出现的位置并往后移3位，去掉id=这部分
        end_index = id_value.find('\'', start_index)  # 从id=后面开始找单引号，确定id值的结束位置
        extracted_id = id_value[start_index:end_index]
        # 每个艺术家的URL
        url = "https://www.artlib.cn/artist_detail?id={}".format(extracted_id)
        # 发送GET请求获取网页内容
        response = requests.session()
        response = response.get(url, headers=params)
        # 设置响应的编码为合理的编码格式，避免乱码问题
        response.encoding = response.apparent_encoding

        # 使用lxml的etree解析网页内容，得到一个可以使用xpath的对象
        html = etree.HTML(response.text)
        person_items = html.xpath('//div[@class="col-md-5"]/div/text()')
        person_yishu = html.xpath('//div[@class="col-md-7"]/div/text()')
        lishi = html.xpath('//div[@class="col-md-7"]/div/p/text()')
        print(person_items, person_yishu, lishi)