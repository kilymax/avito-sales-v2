import os
import re
import cv2
from time import sleep
import requests
import pandas as pd
from datetime import *
from bs4 import BeautifulSoup as BS
from playwright.sync_api import sync_playwright
from tqdm import trange
from transliterate import translit
from requests_html import HTMLSession

# my modules
# from donor_checkers.utils.image_tools import format_image, perturb_image
# from donor_checkers.utils.yandex_api import get_new_link, upload_file

filename = f"app\kraton\kraton"
df = pd.read_excel(f"{filename}.xlsx", dtype={'Article': str}, sheet_name='Лист1')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    counter = 0
    init_length = len(df['Article'])
    for i in range(init_length)[:]:
        art = df.loc[i, 'Article']
        url = f"https://kratonshop.ru/rasshirennyy.htm?searchid=2764746&text={art}&web=0"
        if pd.isna(df.loc[i, 'Title']):
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=10000)

                # Ждём появления iframe на странице
                iframe_element = page.wait_for_selector("iframe[src*='site.yandex.ru/search/site/catalog']", timeout=15000)
                
                # Достаём значение src (ссылку на яндекс страницу)
                iframe_src = iframe_element.get_attribute("src")
                index = i

                # извлекаем ссылку на товар внутри сайта
                ya_page_html = BS(requests.get(iframe_src).content, 'html.parser')
                kraton_product_links = [elem.find("a", {"class": "link link_external_yes link_counter_yes"})['href'] for elem in ya_page_html.find_all("div", {"class": "serp-item__content"})]
                if len(kraton_product_links) > 0:
                    for l in range(len(kraton_product_links)):
                        print(f"Артикул {art} ({i}/{init_length}): {kraton_product_links[l]}")

                        # работаем со страницей продукта на kratonshop.ru
                        kraton_product_html = BS(requests.get(kraton_product_links[l]).content, 'html.parser')

                        # article
                        article = kraton_product_html.find("table", {"style": "HEIGHT: 32px; WIDTH: 1168px"}).find_all("strong")[0].text.strip()
                        if article != art and article not in df["Article"]:
                            index = len(df)
                            df.loc[index, 'Article'] = article

                        # наименование
                        name = kraton_product_html.find("div", {"itemprop": "name"}).text.strip()

                        # мета описание
                        meta_desc = kraton_product_html.find("meta", {"name": "description"})['content'].strip().replace(' ', ' ')

                        # мета ключевые слова
                        meta_keywords = kraton_product_html.find("meta", {"name": "keywords"})['content'].strip().replace(' ', ' ')

                        # описание
                        description_tag = kraton_product_html.find("table", {"style": "HEIGHT: 16px; WIDTH: 1155px"})

                        # изображения
                        images_tags = description_tag.find_all("a", {"class": "highslide"})
                        images = [f"https://kratonshop.ru/{elem['href']}" for elem in images_tags if 'iucatal' in elem['href']]
                        try:
                            images_tags[0].parent.decompose()
                        except:
                            pass

                        # если только одно основное изображение
                        if len(images) < 1:
                            images = [f"https://kratonshop.ru/{elem['href']}" for elem in kraton_product_html.find_all("a", {"class": "highslide"}) if '1_' in elem['href']]

                        # достаем изображения из описания
                        images += [f"https://kratonshop.ru/{elem['src']}" for elem in description_tag.find_all("img")]

                        # отчищаем от ссылок
                        for a in description_tag.find_all("a"):
                            if "href" in a.attrs:
                                del a["href"]
                                del a["target"]

                        # print('title: ', name)
                        # print('meta_desc: ', meta_desc)
                        # print('meta_keywords: ', meta_keywords)
                        # print('images: ', images)
                        # print('desciption: ', description_tag)

                        df.loc[index, 'Title'] = name
                        df.loc[index, 'Link'] = kraton_product_links[l]
                        df.loc[index, 'Meta Description'] = meta_desc
                        df.loc[index, 'Meta Keywords'] = meta_keywords
                        df.loc[index, 'Images'] = ",".join(images)
                        df.loc[index, 'Description'] = str(description_tag)
                        counter += 1

                        if counter % 200 == 199:
                            print("Сохранение...")
                            df.to_excel(f'{filename}_new.xlsx', sheet_name='Лист1', index=False)
                else:
                    try:
                        empty_msg = ya_page_html.find("div", {"class": "serp-messages__message serp-messages__message_type_empty-results"}).find(string=True, recursive=False).strip()
                        df.loc[index, 'Title'] = empty_msg
                    except:
                        df.loc[index, 'Title'] = 'Ошибка'
                        
            except Exception as e:
                print(f"Ошибка с этим артикулом {art} ({url}): {e}")
        
    browser.close()
    print("Сохранение...")
    df.to_excel(f'{filename}_new.xlsx', sheet_name='Лист1', index=False)
    