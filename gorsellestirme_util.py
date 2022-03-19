import numpy as np
import pandas as pd
import pickle
import streamlit as st
import base64

def matrix_reader( alan = "din" ):
    assert alan in ["din", "felsefe"]
    co_occurrence_matrix = np.load("./database/%s_dizin_matrix.npy"%alan )
    with open("./database/%s_dizin_kelimeler.pickle"%alan , "rb") as f:
        dizin_kelimeler = pickle.load(f)
    
    """
    #TODO Kaldırılacak
    kelime_referansı  = []
    for i , j in  enumerate(dizin_kelimeler ) :
        kelime_referansı.append(i)
    """

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
    unsafe_allow_html=True
)
    return out


def word_filter(df, x="din"):
    swap3 = [x in i for i in df.dizin]
    return df.loc[swap3].to_dict("records")

def word_df_creator(df, x):
    swap4 = [x in i for i in df.dizin]
    return df.loc[swap4]

def df_to_wordlist(df, x):
    swap5 = [x in i for i in df.dizin]
    df.loc[swap5]


def filter_callback(**filters):
    
    st.warning(" Filtreleme Özellilği Geçici Bir Süre İçin Kullanım Dışıdır")
    search = ""
    for key in filters.keys() :
        
        if key == "yil":
            search += "self.word_df.yil >= {} & self.word_df.yil <= {} ".format(filters[key][0], filters[key][1])

        elif filters[key] != "Tümü":
            search += "& self.word_df['{}'] == {} ".format(key, filters[key])

    filtered_df = eval( "self.word_df.loc[{}]".format(search)  )

class Plotter:
    def __init__(self, word, df):
        self.word = word
        self.main_df = df


    def secim(self, ):
        pass

class Searcher:

    def __init__(self, word, df):
        self.word = word
        self.main_df = df
        self.word_df = word_df_creator( df, word)
        self.word_df.yil = self.word_df.yil.astype(dtype=int)
        self.word_list = df_to_wordlist(self.word_df, self.word)
        #self.yazar_listesi =  self.word_df.yazar.values


    def word_list(self):
        self.word_list = word_list
        #swap3 = [ self.word in i for i in self.main_df.dizin]
        
        #self.word_df = self.main_df.loc[swap3].to_dict("records")
        pass

    def filter_callback( self, **filters ):
        global filtered_df

        st.warning(" Filtreleme Özellilği Geçici Bir Süre İçin Kullanım Dışıdır")
        search = ""
        count = 0
        for key in filters.keys() :
            if count != 0 and filters[key] != "Tümü":
                search += " & "
            
            count += 1
            if key == "yil":
                search += "(self.word_df.yil >= {}) & (self.word_df.yil <= {})".format(filters[key][0], filters[key][1])

            elif filters[key] != "Tümü":
                search += "(self.word_df['{}'] == {})".format(key, filters[key])

        filtered_df = eval( "self.word_df.loc[{}]".format(search)  )
        
        return filtered_df

        
    def yil(self, yillar ):
        self.yillar = yillar
        
        self.word_df.yil.astype(dtype=int)
        yil_araligi = self.word_df.yil.to_list()
        yil_araligi = list(set(yil_araligi))
        self.yil_araligi = yil_araligi.sort()

        "word_df[ (word_df.yil > yillar[0]) & (word_df.yil < yillar[-1]) ]"


    def parser(self):

        """

        search_terms = [ i for i in swap_1 if i is not None   ]
        filtering_df = self.word_df
        
        for i in search_terms:
            filtering_df = eval("word_df.loc[ word_df.{} == self.{} ]".format( str(i) , str(i) ) )

        
        #"word_df[ (word_df.yil > yillar[0]) & (word_df.yil < yillar[-1]) ]"
        
        self.filtered_df = filtering_df[ (self.word_df.yil > yillar[0]) & (self.word_df.yil < yillar[-1]) ]

        return self.filtered_df
        """
        pass

    def df_returner(self):
        self.parser()

"""

    def extract_word_list(self, df):
        
        
        search_string = "df.loc[{}]".format()
        
        swap6 = [ df.dizin.values ] 
        words = set( swap6 )
        
        pass
        
    def yazar(self, yazar = None):
        if yazar is not None:
            self.yazar = yazar
        
        "word_df.yazar == self.yazar"

        #self.word_df.loc[ word_df.yazar == yazar ]

    def tur(self, tur):
        self.tur = tur

        "word_df.tur == self.tur"


    def yer(self, yer):
        self.yer = yer

        "word_df.yer == self.yer"

    def danisman(self, danisman):
        self.danisman = danisman

        "word_df.danisman == self.danisman"
"""

"""
def searcher(**filters):
    #yil=None, tur=None, yazar=None, danisman=None, yer=None
    danisman_ara = filters.get("danisman", None)
    yer_ara = filters.get("yer", None )
    yazar_ara = filters.get("yazar", None)
    tur_ara = filters.get(tur, None)

    if danisman_ara != None:

    elif yer_ara != None:

    elif yazar_ara != None:

    elif tur_ara != None:

    elif yil_ara != None:
    #for key, value in filters:


df = year_filter()"""

"""
class Displayer:
    def __init__(self, word, df):
        self.word = word
        self.main_df = df
        self.word_df = word_df_creator( df, word)
        
    def standard_displayer(self):
        self.search_buttons = {"yazar": list( set(self.word_df.yazar.values) ) , 
                          "tur": list( set(self.word_df.tur.values) ) ,
                          "yer": list( set(self.word_df['yer bilgisi'].values) ) ,
                          "danisman": list ( set(self.word_df.danisman.values) )
                          }

        for key, value in self.search_buttons.items():
            value.insert(0, "Tümü" )


    def table_display(self, filters = dict, df = pd.DataFrame):
        
        search_string = ""
        
        for i in filters:
            search_string.append( filters[i] )
        
        search_string.sort()

        #df.loc [ df. ]
"""
