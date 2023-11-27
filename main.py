import tkinter as tk
from tkinter import ttk
import requests
import datetime
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html

class QiitaScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Qiita Scraper App")
        root.geometry("480x240")

        # ウィジェットの作成
        self.label_page = ttk.Label(root, text="ページ数(1ページ10件):")
        self.label_tag = ttk.Label(root, text="タグ(複数指定時はカンマ区切り):")
        self.entry_page = ttk.Entry(root, width=40)
        self.entry_tag = ttk.Entry(root, width=40)
        self.button_scrape = ttk.Button(root, text="スクレイピング開始", command=self.scrape_qiita)
        self.status_label = ttk.Label(root, text="スクレイピング結果:")

        # ウィジェットの配置
        self.label_page.grid(row=0, column=0, padx=5, pady=5)
        self.entry_page.grid(row=0, column=1, padx=5, pady=5)
        self.label_tag.grid(row=1, column=0, padx=5, pady=5)
        self.entry_tag.grid(row=1, column=1, padx=5, pady=5,)
        self.button_scrape.grid(row=2, column=0, columnspan=2, pady=10)
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)

    def scrape_qiita(self):
        # フォームのページ数を取得
        pages = self.entry_page.get()
        # フォームのタグを取得
        tags = self.entry_tag.get()

        # スクレイピング先URL
        base_url = 'https://qiita.com'

        try:
            titles = []
            urls = []

            # 指定されたページ数分スクレイピングする
            for page in range(1, int(pages) + 1):
                # スクレイピング先のURLにパラメータ付与
                url = f'{base_url}/search?sort=created&q=tag:{tags}&page={page}'

                # スクレイピング
                response = requests.get(url)
                
                # DOMツリーを作成 
                parsed_html = BeautifulSoup(response.text, 'html.parser')

                # xpathを使用できるように変換
                converted_html = html.fromstring(str(parsed_html))

                # 投稿を抽出
                articles = converted_html.xpath('//article')

                for article in articles:
                    # タイトルを取得
                    titles.append(article.xpath('.//h2/a/text()')[0])
                    # リンクを取得
                    urls.append(base_url + article.xpath('.//h2/a/@href')[0])

            # Excelファイルへの保存
            now = datetime.datetime.now()
            df = pd.DataFrame({'タイトル': titles, 'URL': urls})
            df.to_excel(f"qiita_data{now.strftime('%Y%m%d%H%M%S')}.xlsx", index=False)

            self.status_label.config(text="成功しました。")
        except Exception as e:
            self.status_label.config(text=f"エラー: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QiitaScraperApp(root)
    root.mainloop()
