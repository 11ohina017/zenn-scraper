#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Zenn スクレイパー

"""

import requests
import json
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

def create_html_table(table_head, table_data):
    """HTMLのテーブルを作成

    Args:
        table_head (string): テーブルのヘッダ部分
        table_data (string): テーブルデータ部分
    Returns:
        string: HTML形式のテーブル
    """
    table = '        <table class="tablesorter" id="sort-table" border="2" style="border-collapse: collapse; border-color: blue">'
    table = table + '\r\n        <thead>\r\n'  + table_head + '\r\n        </thead>' + table_data + '\r\n</table>'

    return table

def create_html_table_data(list, tag):
    open_tag = '            <' + tag +'>'
    close_tag = '</' + tag +'>'
    table_data = '\r\n              <tr>'

    for sublist in list:
        table_data =  table_data +  '\r\n      ' + open_tag + sublist + close_tag

    table_data = table_data + '\r\n              </tr>'

    return table_data

# 取得対象ページを初期化
page_number = 1
header_list = ["title", "user", "price", "likedCount", "createdAt", "publishedAt", "sourceRepoUpdatedAt"]

book_row = ''

# Nextページがなくなるまで、1ページづつ取得
while page_number != None:
    load_url = "https://zenn.dev/books?order=latest&page=" + str(page_number)
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")

    # 本の一覧を取得
    for script in soup.find_all("script", id="__NEXT_DATA__"):
        script_dict = json.loads(script.getText())
        page_props_dict = script_dict["props"]["pageProps"]

        # 本の1冊のプロパティを表示
        for book in page_props_dict["books"] :

            book_title = str(book["title"])
            img = '<h4>' + book_title + '</h4><img src="' + str(book["coverImageSmallUrl"]) + '"' + ' title="' + book_title + '" onload="this.width = this.width*0.6">'
            book_props = [img, str(book["user"]['name']), str(book["price"]), str(book["likedCount"]), str(book["createdAt"]), str(book["publishedAt"])
                ,str(book["sourceRepoUpdatedAt"])]

            book_row = book_row + create_html_table_data(book_props, 'td')

        print(book_props)
        # 次ページの番号を取得
        page_number = page_props_dict["nextPage"]
        print("Next Page : " + str(page_number))

L = ['one','two','three','four','five','six','seven','eight','nine']

f = open('zenn_books.html', 'w', encoding='UTF-8')
table = create_html_table(create_html_table_data(header_list, 'th'), book_row)
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
template  = env.get_template('template.html')
replace_data = {'table': table}
html = template .render(replace_data);
print(html)
f.write(html)
f.close()