
import streamlit as st
import numpy as np
from numpy import log  
import pandas as pd
import plotly.graph_objs as go
import base64

from gorsellestirme_util import matrix_reader, set_bg
matrix, kelime_listesi, df = matrix_reader() # din veya felsefe


def plotter(secilen_kelime = "din"):
    
    global mesafe_grup, ids, distances, tags, radials, sizes, hover_text, secim_index, secim_size, secim_cap, secim_tag, secim_distance, secim, karsilasmalar
    
    secim = secilen_kelime
    secim_index = kelime_listesi.index(secilen_kelime)  
    secim_size = matrix[secim_index][secim_index]
    secim_cap = secim_size
    if secim_size >= 100:
        secim_cap = 100
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
        swap8.append(secim_cap + int(i) )
            #hover_text.append( tags[i][j] + '\n' + str(sizes[i][j]) )
            
        distances['%s' %i] = swap8
        
    #return mesafe_grup,ids,distances,tags,radials,sizes

def word_filter(x="din"):
    swap3 = [x in i for i in df.dizin]
    return df.loc[swap3].to_dict("records")

def express(secim='din'):
    
    plotter(secim)

    global fig

    #fig = go.Figure(layout= go.Layout(autosize=False, width=800, height=800) ) # sizes["4"], marker_sizemode= 'area' #calismazsa burayı ac
    fig = go.FigureWidget( ) 
    
    fig.layout  
    fig.add_trace(go.Scatterpolar(r= (0,0) , mode= 'markers', marker_size= secim_cap , marker_symbol='octagon-dot' ,hoverinfo= 'name + text', text = "Tez Sayısı: {}".format(int(secim_size)) , name= secim, marker_sizemode= 'area', showlegend = False   ))

    for i in mesafe_grup:
        i = str(i)
        fig.add_trace( go.Scatterpolar(r= distances[i], theta=radials[i], mode= 'markers', marker_size= sizes[i], hoverinfo= "text", text= tags[i] , marker_sizemode= 'area', showlegend = False ))
        
    #fig.layout.paper_bgcolor = '#000000'
    #fig.layout.polar.radialaxis.showgrid = False
    fig.layout.polar.radialaxis.visible = False
    fig.update_layout(template = "plotly", xaxis_showgrid=False, yaxis_showgrid=False, margin=go.layout.Margin(l=0,r=0, b=0, t=0), title=secim, paper_bgcolor="rgba(0,0,0,0)" ) # paper_bgcolor=' #0000b3 # templates=["ggplot2", "saborn", "plotly", plotly_dark ]
    

    return fig

def callback(trace, points, selector):
    inds = points.point_inds
    return inds.text

 

st.set_page_config(page_icon="./icon2.png", page_title="YOKTEZ Bağlam Haritası")
set_bg("./media/bg.jpg")
st.markdown("___ ")


sec = st.selectbox(label="Kavram Seçiniz", options=kelime_listesi, index=2505)

st.markdown("___ ")

st.plotly_chart( express(sec) )

st.markdown("___ ")

#st.slider("%s Yıl Seçin:" %secim.upper(), ) 

#st.table(word_filter('din') )   

st.dataframe( word_filter( sec ) )
