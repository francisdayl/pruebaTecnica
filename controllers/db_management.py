import sqlite3
import pandas as pd
from os import path



def jaccard_similarity(set1:list, set2:list):
    set1,set2=set(set1),set(set2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity = intersection / union
    return similarity


def create_db():
    if not path.exists('school_data.db'):
        df_db = pd.read_csv('school_data.csv',encoding='cp1252')
        conn = sqlite3.connect('school_data.db')
        curs = conn.cursor()
        curs.execute('''CREATE TABLE Schools (id int PRIMARY KEY , name char, city char, state char )''')
        conn.commit()

        df_data = pd.DataFrame({'id':df_db['NCESSCH'].values, 'name':df_db['SCHNAM05'].values 
                        , 'city':df_db['LCITY05'].values, 'state':df_db['LSTATE05'].values })
        
        df_data.to_sql('Schools', conn, if_exists='replace')
        conn.commit()
        conn.close()
    pass


def school_search(text:str):
    conn = sqlite3.connect('school_data.db')
    curs = conn.cursor()
    text_list = text.upper().split(" ")

    list_filters = list(map(lambda palabra: f' name LIKE "%{palabra}%" OR', text_list))
    word_filters = "".join(list_filters)
    query = f'''SELECT name, city, state FROM Schools WHERE {word_filters[:-2]}'''

    sql_query = pd.read_sql(query, conn)
    df = pd.DataFrame(sql_query, columns = ['name', 'city', 'state'])
    df['sort_value'] = df['name'].apply(lambda x: jaccard_similarity(x.split(" "),text_list))
    df_sorted = df.sort_values(by='sort_value',ascending=False)[:3]
    result = {}
    for i in range(3):
        row = df_sorted.iloc[i].values
        result[f'{i+1}']= f'{row[0]} - {row[1]},{row[2]}'
    conn.commit()
    conn.close()
    return result








