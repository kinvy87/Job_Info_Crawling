
m flask import Flask app=Flask(__name__)@app.route("/")def hello(): return "hello World!"if __name__=="__main__": app.run(host="0.0.0.0",port=8080,debug=True)
rt urllib.request

import urllib.parse

import time

from bs4 import BeautifulSoup





class Zhilian(object):

    def __init__(self, jl, kw, start_page, end_page):

        # 保存到成员属性中，其他方法中才能直接使用

        self.jl = jl

        self.kw = kw

        self.start_page = start_page

        self.end_page = end_page

        self.items = []



    def handle_request(self, page):

        data = {

            'jl': self.jl,

            'kw': self.kw,

            'p': page,

        }

        query_string = urllib.parse.urlencode(data)

        url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?'

        url += query_string



        headers = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

        }

        request = urllib.request.Request(url=url, headers=headers)

        return request



    def parse_content(self, content):

        soup = BeautifulSoup(content, 'lxml')

        table_list = soup.find_all('table', class_='newlist')[1:]

        # print(table_list)

        print(len(table_list))

        for table in table_list:

            zwmc = table.select('.zwmc a')[0].text.strip('\xa0')

            gsmc = table.select('.gsmc a')[0].text

            zwyx = table.select('.zwyx')[0].text

            gzdd = table.select('.gzdd')[0].text



            gwxq = table.find('li', class_='newlist_deatil_two').text.strip('\xa0')

            jtyq = table.find('li', class_='newlist_deatil_last').text.strip('\xa0')



            item = {

                '职位名称：': zwmc,

                '公司名称：': gsmc,

                '职位月薪：': zwyx,

                '工作地点：': gzdd,

                '岗位详情：': gwxq,

                '具体要求：': jtyq,

            }

            print(item)

            self.items.append(item)

            time.sleep(1)



    def run(self):

        for page in range(self.start_page, self.end_page + 1):  # 可直接调用成员属性

            print('正在爬取第%s页......' % page)

            request = self.handle_request(page)  # 构建请求对象

            content = urllib.request.urlopen(request).read().decode('utf8')

            self.parse_content(content)  # 解析返回的内容

            print('完成爬取')

            time.sleep(2)



        info = str(self.items)  # write()内的参数是字符串格式

        # 将所有的工作保存到文件中

        with open('ZhiLian.txt', 'w', encoding='utf8') as fp:

            fp.write(info)





def main():

    # 工作地点

    jl = input('请输入工作地点：')

    # 工作种类

    kw = input('请输入工作种类：')

    # 起始页码

    start_page = int(input('请输入起始页码：'))

    # 结束页码

    end_page = int(input('请输入结束页码：'))



    # 创建对象

    zhilian = Zhilian(jl, kw, start_page, end_page)

    # 通过对象调用类方法

    zhilian.run()





if __name__ == '__main__':

    main()
