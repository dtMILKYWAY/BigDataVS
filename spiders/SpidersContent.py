import random

import requests
from lxml import etree

import mysql.connector


def insert_artwork_data(artwork_data):
    # 爬取的数据

    # 解析数据
    name = None
    foreign_name = None
    time = None
    author = None
    texture = None
    work_type = None
    institution=None
    period = None
    description = None
    for item in artwork_data:
        if item.startswith('名称：'):
            name = item[3:].strip()
        elif item.startswith('作者：'):
            author = item[3:].strip()
        elif item.startswith('外文名称：'):
            foreign_name = item[5:].strip()
        elif item.startswith('创作时间：'):
            time = item[5:].strip()
        elif item.startswith('材质：'):
            texture = item[3:].strip()
        elif item.startswith('作品类型：'):
            work_type = item[5:].strip()
        elif item.startswith('收藏机构：'):
            institution = item[5:].strip()
        elif item.startswith('艺术时期：'):
            period = item[5:].strip()
        elif item.startswith('作品描述：'):
            description = item[5:].strip()
    # 处理可能的 None 值
    # 数据库连接信息，根据实际情况修改
    config = {
        'host': 'localhost',
        'database': 'bysj',
        'user': 'root',
        'password': '123456'
    }
    try:
        # 连接数据库
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            # SQL 插入语句
            sql = ("INSERT INTO ArtWork (Name, ForeignName, time,Author,  Texture, Type, institution,Period, description) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            # 插入数据
            val = (name, foreign_name, time,author,  texture, work_type,institution, period, description)

            cursor.execute(sql, val)
            connection.commit()
            print("数据插入成功")
    except mysql.connector.Error as e:
        print(f"数据插入失败: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接关闭")


if __name__ == "__main__":
    a=50
    population = range(1, 8645)
    random_numbers = random.sample(population, 30)
    random_numbers=[4455,3355]

    print(random_numbers)
    for b in range(a):
        x=random_numbers[b]
        print("第{}页".format(x))
        url='https://www.artlib.cn/artwork_list?page={}'.format(x)
        # #手动登录后，f12拿到cookie值
        params = {
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "cookie":"gfsessionid=14rp7hcaj6db60d6ou8k0cz672hn1qy3"

        }

        # 发送GET请求获取网页内容
        response = requests.session()
        response=response.get(url,headers=params)
        # print(response)
        # 设置响应的编码为合理的编码格式，避免乱码问题
        response.encoding = response.apparent_encoding

        # 使用lxml的etree解析网页内容，得到一个可以使用xpath的对象
        dhtml = etree.HTML(response.text)

        #获取这一页有多少个艺术画
        div_count = len(dhtml.xpath('//div[@class="data-list"]/div'))
        print(div_count)
        for i in range(div_count):
            #得到网页地址
            id_value= dhtml.xpath('//div[@class="data-list"]/div/@onclick')[i]
            start_index = id_value.find('id=') + 3  # 找到id=出现的位置并往后移3位，去掉id=这部分
            end_index = id_value.find('\'', start_index)  # 从id=后面开始找单引号，确定id值的结束位置
            extracted_id = id_value[start_index:end_index]
           # 每个艺术画的URL
            url = "https://www.artlib.cn/artwork_detail?id={}".format(extracted_id)
            # 发送GET请求获取网页内容
            response = requests.session()
            response = response.get(url, headers=params)
            # 设置响应的编码为合理的编码格式，避免乱码问题
            response.encoding = response.apparent_encoding

            # 使用lxml的etree解析网页内容，得到一个可以使用xpath的对象
            html = etree.HTML(response.text)
            html_str = etree.tostring(html, encoding='utf-8').decode('utf-8')
            # print(html_str)
            divs = html.xpath('//div[@class="col-md-3 left"]/div')
            result_list = []
            for div in divs:
                text_content = div.xpath('string()').replace('\r', '').replace('\n', '').replace('\t', '').replace("     ",'').strip()
                result_list.append(text_content)

            print(result_list)
            insert_artwork_data(result_list)