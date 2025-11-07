import pandas as pd
from tqdm import trange

new_file = "app\kraton\kraton"
old_file = "app\kraton\\tovary_new"
new_df = pd.read_excel(f"{new_file}.xlsx", dtype={'Article': str}, sheet_name='Лист1')
old_df = pd.read_excel(f"{old_file}.xlsx", dtype={'Код_товара': str}, sheet_name='Лист1')
old_art_list = list(old_df['Код_товара'])

for i in trange(len(new_df.index)):
    new_art = new_df.loc[i, 'Article']
    for j in range(len(old_df.index)):
        if old_df.loc[j, 'Количество'] != 1: # временно
            index = j
            old_art = old_df.loc[index, 'Код_товара']
            if new_art not in old_art_list:
                index = len(old_df.index)
                old_df.loc[index, 'Ссылка_изображения'] = f"{new_df.loc[i, 'Images']}"
                old_df.loc[index, 'Количество'] = 1
                old_df.loc[index, 'Код_товара'] = new_df.loc[i, 'Article']
                old_df.loc[index, 'Детальное_описание'] = new_df.loc[i, 'Description']
                old_df.loc[index, 'Мета_Заголовок'] = new_df.loc[i, 'Title']
                old_df.loc[index, 'Мета_Ключевые_слова'] = new_df.loc[i, 'Meta Keywords']
                old_df.loc[index, 'Мета_Описание'] = new_df.loc[i, 'Meta Description']
                break
            if new_art == old_art:
                old_df.loc[index, 'Ссылка_изображения'] = f"{new_df.loc[i, 'Images']},{old_df.loc[index, 'Ссылка_изображения']}"
                old_df.loc[index, 'Количество'] = 1
                old_df.loc[index, 'Код_товара'] = new_df.loc[i, 'Article']
                old_df.loc[index, 'Детальное_описание'] = new_df.loc[i, 'Description']
                old_df.loc[index, 'Мета_Заголовок'] = new_df.loc[i, 'Title']
                old_df.loc[index, 'Мета_Ключевые_слова'] = new_df.loc[i, 'Meta Keywords']
                old_df.loc[index, 'Мета_Описание'] = new_df.loc[i, 'Meta Description']
                break


old_df.to_excel(f'{old_file}_new.xlsx', sheet_name='Лист1', index=False)


            
            
            
            
            

