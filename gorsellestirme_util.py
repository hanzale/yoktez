from mimetypes import init
from turtle import update
from webbrowser import get
import numpy as np
import pandas as pd
import pickle
import streamlit as st
import base64

def matrix_reader( alan = "din" ):
    assert alan in ["din", "felsefe"]
    co_occurrence_matrix = np.load("./database/%s_dizin_matrix.npy"%alan )

    #TODO remove & use Searcher.word_list instead
    with open("./database/%s_dizin_kelimeler.pickle"%alan , "rb") as f:
        dizin_kelimeler = pickle.load(f)
    
    with open("./database/%s_duzenli_dataframe.pickle"%alan , "rb") as f:
        df = pd.read_pickle(f)
    
    return co_occurrence_matrix, dizin_kelimeler, df

def set_bg(img):

    st.set_page_config(page_icon="./media/icon2.png", page_title="YOKTEZ Bağlam Haritası") #, layout="wide"

    main_bg = img
    main_bg_ext = img.split('.')[-1]

    out = st.markdown(
   f"""
        <style>
        .reportview-container {{
            background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
        }}
        .sidebar .sidebar-content {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
        }}
        </style>
    """, 
        unsafe_allow_html=True )
    return out

def word_filter(df, x="din"):
    swap3 = [x in i for i in df.dizin]
    return df.loc[swap3].to_dict("records")


class Searcher:

    def __init__(self, word, df):
        self.word = word
        self.main_df = df
        self.load(self.word, self.main_df)

    def load(self, word, df):
        self.word_df = self.word_df_creator( df, word )
        self.word_list = self.df_to_wordlist( self.word_df, word )
        self.year_list = self.year_handler( self.word_df )

    def update(self, df):
        self.load(self.word, df)

    def word_df_creator(self, df, x):
        swap4 = [x in i for i in df.dizin]
        word_df = df.loc[swap4]
        word_df.yil = word_df.yil.astype(dtype=int)
        return word_df

    def df_to_wordlist(self, df, x):
        swap5 = [x in i for i in df.dizin]
        swap6 = df.dizin.loc[swap5].tolist()
        return  list( set( [ item for sublist in swap6 for item in sublist] ) ) 
        
    def year_handler(self, df):
        year_list = sorted(list(set(df.yil.values.tolist())))
        if len(year_list) == 1:
            year_list.append( year_list[0]+1 )
        
        return year_list

    def filter_callback( self, **filters ):
        

        st.warning(" Filtreleme Özellilği Deneme Sürecindedir")

        filtered_df = self.word_df

        for key in filters.keys() :

            if key == "yil":
                filtered_df = filtered_df.loc[ 
                        (self.word_df.yil >= int( filters[key][0] ) )& 
                        (self.word_df.yil <= int( filters[key][1] ) )
                ]

            elif filters[key] != "Tümü":
                filtered_df  = filtered_df.loc[
                    (self.word_df[key] == filters[key])
                ]
        
        return filtered_df


class Plotter(Searcher):
    def __init__(self, word, df):
        Searcher.__init__(word, df)
        self.reference_df = self.main_df
        self.plot_df = self.word_df


"""
TODO Veri tabanı SQL formatıyla ayrıca kaydedilecek.
TODO YÖKTEZ veritabanına erişim & api izni alınacak.
"""