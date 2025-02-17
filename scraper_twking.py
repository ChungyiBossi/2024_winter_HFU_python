from pprint import pprint
import requests
from bs4 import BeautifulSoup

# Step 1: request & parse
url = "https://www.twking.cc/"
r = requests.get(url)
r.encoding = 'utf8'  # 避免亂碼
soup = BeautifulSoup(r.text, 'html.parser')
# print(len(r.text))


# Step 2: 找訊息
# soup.find_all('div', class_='booktop')
booktops = soup.find_all('div', attrs={"class": "booktop"})
for booktop in booktops:
    # sol.1
    tops = booktop.find_all('p')
    top_type = tops[0].text  # 哪種top10?
    print(top_type)
    for top in tops[1:]:
        print('\t', top.a.text, ':', top.a.get('href'))

    # # sol.2
    # top_type = booktop.p.text
    # tops = booktop.css.select('p a')  # 小說
    # print(top_type)
    # for top in tops:
    #     print('\t', top.text, ':', top.get('href'))


# Step 3: collection
booktop_summarize = dict()
booktops = soup.find_all('div', attrs={"class": "booktop"})
for booktop in booktops:
    tops = booktop.find_all('p')
    for top in tops[1:]:
        top_book_name = top.a.text  # 小說名稱
        top_book_url = top.a.get('href')  # 小說的連結

        if top_book_name in booktop_summarize:
            booktop_summarize[top_book_name]['count'] += 1  # 已存在在紀錄中
        else:
            booktop_summarize[top_book_name] = {
                'count': 1,
                'href': top_book_url
            }

pprint(booktop_summarize)
