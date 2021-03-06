import urllib.parse
import pandas as pd
from tqdm import tqdm

target_lang = 'hu'
wiki_page = f'https://sv.wiktionary.org/wiki/'


def translate():
    j = 1

    excel_df = pd.read_excel('data.xlsx', index_col=0)

    for index, row in tqdm(excel_df.iterrows(), total=len(excel_df)):
        index_size = len(index.split())
        j += 1
        try:
            if index_size <= 1:
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
            else:
                df = pd.read_html(wiki_page + urllib.parse.quote(index.split()[-1]))
                i = 0
                while not 'Singular' in df[i].columns:
                    i += 1

                word_dict = dict(zip(['Singular', 'Plural'], [df[i]['Singular'].iloc[:,0][0], df[i]['Plural'].iloc[:,0][0]]))
                excel_df.loc[index] = [word_dict.get('Singular'), word_dict.get('Plural'), "-", "-", f'=GOOGLETRANSLATE(A{j} ; "sv"; "en")',
                                       f'=GOOGLETRANSLATE(A{j} ; "sv"; "{target_lang}")']

        except Exception as e:
            excel_df.loc[index] = ["-", "-", "-", "-", f'=GOOGLETRANSLATE(A{j} ; "sv"; "en")', f'=GOOGLETRANSLATE(A{j} ; "sv"; "{target_lang}")']
            print(index, row, word_dict, e)
            pass
    print(excel_df)
    writer = pd.ExcelWriter('done.xlsx', engine='xlsxwriter')
    excel_df.to_excel(writer, sheet_name='translations')

    work_sheet = writer.sheets['translations']
    work_sheet.set_column(1, 6, 20)
    writer.save()


if __name__ == "__main__":
    print("Translating started for rows:\n")
    translate()
    print("Done.")
