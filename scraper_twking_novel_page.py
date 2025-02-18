import pandas as pd
from pprint import pprint
import requests
from bs4 import BeautifulSoup


# Step 1. 讀取主頁排行榜名單
book_tops = pd.read_csv('booktop.csv')
# print(book_tops.head(10))
book_top10s = book_tops.head(10)
for book_top10 in book_top10s.iterrows():
    print(book_top10[1]['novel_name'], book_top10[1]['novel_page_url'])

    # Step 2
    page_url = book_top10[1]['novel_page_url']
    r = requests.get(page_url)
    r.encoding = 'utf8'  # 避免亂碼
    page_soup = BeautifulSoup(r.text, 'html.parser')

    # 取得所有章節的版面節點
    chapter_wrapper = page_soup.find(
        'div',
        attrs={'class': 'info-chapters flex flex-wrap'})

    chapters = chapter_wrapper.find_all('a')
    print(f"{book_top10[1]['novel_name']}, # of chapters: {len(chapters)}")
    last_chapter = chapters[-1]
    print(f"last chapter: {last_chapter.get('title')}")
    print(f"which at {last_chapter.get('href')}")
    print()
