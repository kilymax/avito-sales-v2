import os
import sys
import re
import cv2
from time import sleep
import requests
import pandas as pd
from datetime import *
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as BS
from tqdm import tqdm, trange
from PIL import Image


excel_file_name = "corsel_dvadomkrata"

df = pd.read_excel(f"{excel_file_name}.xlsx", sheet_name='Объявления')


# перестановка артикулов в конец
# words = [
#             "Преобразователь",
#             'Преобразователь',
#             'Бензиновая',
#             'Электрогенератор',
#             'Дизельная',
#             'Жидкотопливный',
#         ]

# for word in words:
#     regex = r'.*(?= ' + word + r')'  # r'.*(?= Опрессовщик)',
#     for i in trange(len(df)):
#         # Изменение тайтла
#         try:
#             part = re.match(regex, title)[0]
#             title = f'{title.replace(part, '').strip()} {part}'
#             print(i, ':', title)
#         except: pass 


#         df.loc[i, 'Title'] = title.strip()



# сокращение тайтла регулярками до 50 символов

# regex = r' \d+\s?л/мин '
# regex = r' \d{1,2}\s?т '12 т
# regex = r' \d*Нм'
# regex = r' \d{4,6} ДГ'
# regex = r' \d{5,7}\s?ДУ'
# regex = r' Д.+ HHYG-'
# regex = r' Инстан ГК.*'
count = 0
for i in trange(len(df)):
    # Изменение тайтла
    title = df.loc[i, 'Title'].replace('!', '').replace('  ', ' ').replace('\n', ' ').strip()
    title = f'{title[0].upper()}{title[1:]}'
    if len(title) > 50:
        
            #     if "ГГМК" in title:
            #         part = re.search(regex, title)[0] 
            #         # title = f'{title.replace(part, '').strip()} {part}'
            #         title = title.replace(part, ' Инстан')
            #         title = title.replace('  ', ' ').strip()
            #         print(i, part)

        if len(title) > 50:
            # фильтрация по символам
            title = '!' + title
            count += 1

    df.loc[i, 'Title'] = title.strip()
print(f'Больше 50 символов тайтлов: {count}')
df.to_excel(f'{excel_file_name}.xlsx', sheet_name='Объявления', index=False)


# """
# part = re.search(' \d+\s?л/мин ', title)[0]

# """