'''
@File   : main.py
@Author : Levi
@Date   : 2021/05/02
@Desc   :
'''
#coding:utf-8
import os
import sys
import requests
import json
import random
import pymysql

sys.path.append(os.getcwd())
from jd_crawler.jd_parser.search import search_item
from jd_crawler.setting import MYSQL_LOCAL_CONF
headers = {
    "cache-control": "max-age=0",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "cookie": "areaId=1;"


}

def save_item(item):
    """
    存储器
    最大999
    :param item:
    :return:
    """
    SQL = "INSERT INTO jd_search(img, price, name, shop, icons, sta_date) VALUES(%s, %s, %s, %s, %s, %s)"
    cursor.executemany(SQL,item)
    mysql_server.commit()

def request_search(keyword):
    """
    下载器
    - 加代理IP
    :param keyword:
    :return:
    """
    url = "https://search.jd.com/Search"
    params = {
       "keyword": keyword, #加了引号就不是传参了
       "psort": 3,
       "wq": keyword,
       "psort": 3,
    }

    #在请求之前加上一个ip代理
    proxy = random.choice(ip_array)
    proxies = {
        "http": f"http://{proxy['ip']}:{proxy['port']}",
        "https": f"https://{proxy['ip']}:{proxy['port']}"
    }

    response = requests.get(url=url, params=params, headers=headers)
    return response.text


def main():
    """
    主函数/调度器
    :return:
    """
    for keyword in keyword_array:
        result = request_search(keyword)
        item_array = search_item(result)
        save_item(item_array)

    print("done!")

if __name__ == "__main__":
    # 代替任务生产者
    mysql_server = pymysql.connect(**MYSQL_LOCAL_CONF)
    cursor = mysql_server.cursor()
    keyword_array = ["键盘", "鼠标", "显示器", "机箱", "显卡"]
    json_data = json.loads("""{"code":0,"data":[{"ip":"59.62.32.168","port":4245},{"ip":"111.77.96.231","port":4271},{"ip":"182.87.172.197","port":4245},{"ip":"113.117.10.20","port":4245},{"ip":"111.77.96.30","port":4271},{"ip":"113.75.138.132","port":4265},{"ip":"183.7.149.206","port":4230},{"ip":"27.44.211.42","port":4213},{"ip":"113.76.59.116","port":4256},{"ip":"115.152.227.101","port":4245},{"ip":"14.115.205.51","port":4246},{"ip":"27.44.218.251","port":4213},{"ip":"59.62.169.97","port":4251},{"ip":"111.77.98.105","port":4261},{"ip":"27.44.216.40","port":4278},{"ip":"27.44.220.121","port":4245},{"ip":"113.64.142.219","port":4245},{"ip":"121.8.28.141","port":4245},{"ip":"182.87.172.254","port":4245},{"ip":"59.62.170.65","port":4273}],"msg":"0","success":true}""")
    ip_array = json_data['data']


    main()