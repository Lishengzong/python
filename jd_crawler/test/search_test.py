from jd_crawler.jd_parser.search import search_item
from pprint import pprint
file = r"D:\pycharmproject\Python\jd_crawler\test\search_test.html"
with open(file, "r", encoding="utf-8") as f:
    result =search_item(f.read())
    pprint(result)