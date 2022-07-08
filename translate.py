import urllib.parse
import pandas as pd
from tqdm import tqdm

target_lang = 'de'
wiki_page = f'https://sv.wiktionary.org/wiki/'


def translate():
    j = 1

    excel_df = pd.read_excel('data.xlsx', index_col=0)

    for index, row in tqdm(excel_df.iterrows(), total=len(excel_df)):
        j += 1
        try:
            df = pd.read_html(wiki_page + urllib.parse.quote(index))
            i = 0
            word_dict = dict(zip(df[i].iloc[:, 0], df[i].iloc[:, 1]))
            while not word_dict.get('Infinitiv'):
                i += 1
                word_dict = dict(zip(df[i].iloc[:, 0], df[i].iloc[:, 1]))
            excel_df.loc[word_dict['Infinitiv']] = [word_dict.get('Presens'), word_dict.get('Preteritum'),
                                                    word_dict.get('Supinum'), word_dict.get('Imperativ'),
                                                    f'=GOOGLETRANSLATE(A{j} ; "sv"; "en")',
                                                    f'=GOOGLETRANSLATE(A{j} ; "sv"; "{target_lang}")']
        except Exception as e:
            print(word_dict, e)
            pass

    writer = pd.ExcelWriter('done.xlsx', engine='xlsxwriter')
    excel_df.to_excel(writer, sheet_name='translations')

    work_sheet = writer.sheets['translations']
    work_sheet.set_column(1, 6, 20)
    writer.save()


if __name__ == "__main__":
    print("Translating started for rows:\n")
    translate()
    print("Done.")
