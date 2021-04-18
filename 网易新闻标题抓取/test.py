import requests
from pyquery import PyQuery as pq
import pandas as pd

url = 'https://news.163.com/'
header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
rep = requests.get(url, headers=header)
doc = pq(rep.text)
new_itme = doc.find("li[ne-role='tab-body'] .hidden div").items()

new_pandas = []

for i in new_itme:
    title = i.find("a").text()
    link = i.find("a").attr("href")
    print(title)
    new_pandas.append(
        {
            '标题': title,
            '链接': link,
        }
    )

df = pd.DataFrame(new_pandas, columns=['标题', '链接'])
# 保存
df.to_csv("news163.csv")


