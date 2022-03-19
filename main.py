from textwrap import indent
from pandas._config.config import options
from pandas.core.indexes.base import Index
import streamlit as st
import numpy as np
from numpy import log  
import pandas as pd
import plotly.graph_objs as go
import base64

from gorsellestirme_util import Searcher, matrix_reader, set_bg


def plotter( kelimeler, secilen_kelime = "din" ):
    
    global mesafe_grup, ids, distances, tags, radials, sizes, hover_text, secim_index, secim_size, secim_cap, secim_tag, secim_distance, secim, karsilasmalar
    
    secim = secilen_kelime
    secim_index = kelime_listesi.index(secilen_kelime)  
    secim_size = matrix[secim_index][secim_index]
    secim_cap = secim_size

    if secim_size >= 100:
        secim_cap = 100
    elif secim_size > 0 and secim_size < 20:
        secim_cap = 50
    secim_tag = secilen_kelime
    secim_distance = 0
    
    
    karsilasmalar = matrix[ secim_index, ]
    karsilasmalar[secim_index] = 0


    mesafe_grup = [ int(i) for i in karsilasmalar if i > 0]
    mesafe_grup = list(set(mesafe_grup))
    mesafe_grup.sort()
    
    ids = {}
    for grup in mesafe_grup:
        swap5 = []
        for index in range(len(karsilasmalar)):
            if karsilasmalar[index] == grup:
                swap5.append(index)
        ids[ '%s' %grup ] = swap5
    
    distances = {} 
    tags = {}    
    radials = {}
    sizes = {}
    #hover_text = []

    for i in ids:
        
        #radial_placement
        swap10 = 360 / len(ids[i]) 
        
        #swap6 = np.arange(0, 360, swap10) #dairede eş aralıklı dağılım
        swap6 = np.random.random_integers(0,360, len( ids[i] ) ) #rastgele dağılım
        
        radials['%s' %int(i)] = swap6
         
        #tags & sizes
        swap7 = []
        swap9 = []
        for j in ids[i]:
            swap7.append( kelime_listesi[j] )
            swap9.append( int( matrix[j,j] ) ) #multiply integer value in order to optimize
        
        swap9 = [i + 50  if i < 50 else 120 for i in swap9]

        tags['%s' %i] = swap7
        sizes["%s" %i] = swap9        
        
        
        #radius length
        swap8 = []

        for j in range(len(ids[i])):
            #swap8.append( 1 - ( 1 /  ( mesafe_grup[-1] - (int(i))) )  )
            swap8.append(  1 -  np.log10(int(i))  )
             
            #hover_text.append( tags[i][j] + '\n' + str(sizes[i][j]) )
            
        distances['%s' %i] = swap8
         
    #return mesafe_grup,ids,distances,tags,radials,sizes

def express(secim='din'):
    
    plotter(secim)

    global fig

    #fig = go.Figure(layout= go.Layout(autosize=False, width=800, height=800) ) # sizes["4"], marker_sizemode= 'area' #calismazsa burayı ac
    fig = go.FigureWidget( ) 
    

    fig.add_trace(go.Scatterpolar(r= (0,0) , mode= 'markers', marker_size= secim_cap , marker_symbol='octagon-dot' ,hoverinfo= 'name + text', text = "Tez Sayısı: {}".format(int(secim_size)) , name= secim, marker_sizemode= 'area', showlegend = False   ))

    for i in mesafe_grup:

        i = str(i)
        fig.add_trace( go.Scatterpolar(r= distances[i], theta=radials[i], mode= 'markers', marker_size= sizes[i], hoverinfo= "text", text= tags[i] , marker_sizemode= 'area', showlegend = True ))
        
    #fig.layout.paper_bgcolor = '#000000'
    #fig.layout.polar.radialaxis.showgrid = False
    fig.layout.polar.radialaxis.visible = False
    fig.update_layout(template = "plotly", xaxis_showgrid=False, yaxis_showgrid=False, margin=go.layout.Margin(l=0,r=0, b=0, t=0), title=secim, paper_bgcolor="rgba(0,0,0,0)" ) # paper_bgcolor=' #0000b3 # templates=["ggplot2", "saborn", "plotly", plotly_dark ]
    

    return fig

"""
def callback(trace, points, selector):
    inds = points.point_inds
    return inds.text
"""

### !!! PAGE UNDER CONSTRUCTION !!! ####
#set_bg("./media/bg.jpg")
st.header("Türkiye Lisansüstü Çalışmaları Bağlam Haritası") 

database = st.sidebar.radio("Veri Tabanı Seçiniz", options= [ "Din" , "Felsefe"])
with open ( "README.md", "r" ) as f:
    txt = f.read()
    st.sidebar.text_area( label = "Tanıtım:", value= txt, height= 500 )

matrix, kelime_listesi, main_df = matrix_reader(database.lower()) # din veya felsefe
main_df.yil.astype(dtype=int)
yil_araligi = main_df.yil.to_list()
yil_araligi = list(set(yil_araligi))
yil_araligi.sort()

st.markdown("___")

sec = st.selectbox(label="Kavram Seçiniz", options=kelime_listesi, index=2505, format_func= str.capitalize,  )
sec = Searcher(sec, main_df)

with st.beta_expander( label="Detaylı Arama", expanded= False ) :
    col1, col2, col3, col4 = st.beta_columns(4)

    yillar          = st.select_slider(label= "Yıl Aralığı Seç", options=  yil_araligi, value=( min(yil_araligi), max(yil_araligi) ) ) 
    danisman_filtre = col1.selectbox  (label= "Danışman Ara",    options= ["Tümü"] + list(set(sec.word_df.danisman.values.tolist() )),       key = "daniss", index = 0 )
    yer_filtre      = col2.selectbox  (label= "Üniversite Ara",  options= ["Tümü"] + list(set(sec.word_df["yer bilgisi"].values.tolist() )), key = "yerr",   index = 0 )
    tur_filtre      = col3.selectbox  (label= "Tür Ara",         options= ["Tümü"] + list(set(sec.word_df.tur.values.tolist() )),                            index = 0 )
    yazar_filtre    = col4.selectbox  (label= "Yazar Ara",       options= ["Tümü"] + list(set(sec.word_df.yazar.values.tolist() )),          key = "yazz",   index = 0 )

    st.button("Filtreleri Uygula", on_click= sec.filter_callback(yil= yillar, yazar= yazar_filtre, danisman=danisman_filtre, yer_bilgisi=yer_filtre) )
    
st.markdown("___ ")

st.plotly_chart( express(sec.word) )

#st.table(  sec.word_df.dizin.values.tolist() ) 
#st.table(sec.word_df.loc[ (sec.word_df.tur == "Yüksek Lisans") & (sec.word_df.yil == "2017")  ])

st.markdown("___ ")

#st.slider("%s Yıl Seçin:" %secim.upper(), ) 
#st.table(filtered_df)
#st.table(word_filter('din') )   

#st.dataframe( word_filter( sec ) )

st.dataframe( sec.word_df )
