import streamlit as st
import numpy as np
import plotly.graph_objs as go


from gorsellestirme_util import Plotter, Searcher, matrix_reader, set_bg

# matrix indexi & kelime listesi indexi üstünde tablolar birleşiyor

def plotter( secilen_kelime = "din" ):

    global mesafe_grup, ids, distances, tags, radials, sizes, hover_text, secim_index, secim_size, secim_cap, secim_tag, secim_distance, karsilasmalar
    
    secim = secilen_kelime
    secim_index = kelime_listesi.index( secim )  
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
        
        #swap6 = np.arange(0, 360, swap10) #dairede eş aralıklı dağılım
        swap6 = np.random.randint(0,360+1, len( ids[i] ) ) #rastgele dağılım
        
        radials['%s' %int(i)] = swap6
         
        #tags & sizes
        swap7 = []
        swap9 = []
        for j in ids[i]:
            swap7.append( kelime_listesi[j] )
            swap9.append( int( matrix[j,j] ) ) #multiply integer value in order to optimize
        
        #swap9 = [k + 50  if k < 50 else 120 for k in swap9]
        swap9 = [k + 60  if k < 50 else k for k in swap9]

        tags['%s' %i] = swap7
        sizes["%s" %i] = swap9        
        
        
        #radius length
        swap8 = []

        for j in range(len(ids[i])):
            #swap8.append( 1 - ( 1 /  ( mesafe_grup[-1] - (int(i))) )  )
            swap8.append( 1 - np.log10(int(i)) + 0.5  )
             
            #hover_text.append( tags[i][j] + '\n' + str(sizes[i][j]) )
            
        distances['%s' %i] = swap8
         
    #return mesafe_grup,ids,distances,tags,radials,sizes

def express(secim='din'):

    plotter(secim)

    global fig
    #fig = go.Figure(layout= go.Layout(autosize=False, width=800, height=800) ) # sizes["4"], marker_sizemode= 'area' #calismazsa burayı ac
    fig = go.FigureWidget( ) 

    fig.add_trace(go.Scatterpolar(  r= (0,0), 
                                    mode= 'markers', 
                                    marker_size= secim_cap, 
                                    marker_symbol='octagon-dot',
                                    hoverinfo= 'name + text', 
                                    text = "Tez Sayısı: {}".format(len(sec.word_df)), 
                                    name = secim, 
                                    marker_sizemode= 'area', 
                                    showlegend = False   
                                    )
                                    )

    for i in mesafe_grup:

        i = str(i)
        fig.add_trace( go.Scatterpolar( r= distances[i], 
                                        theta=radials[i], 
                                        mode= 'markers', 
                                        marker_size= sizes[i], 
                                        hoverinfo= "text", 
                                        text= tags[i], 
                                        marker_sizemode= 'area', 
                                        showlegend= False 
                                        )
                                        )
        
    #fig.layout.paper_bgcolor = '#000000'
    #fig.layout.polar.radialaxis.showgrid = False
    fig.layout.polar.radialaxis.visible = False
    fig.update_layout(template = "plotly", xaxis_showgrid=False, yaxis_showgrid=False, margin=go.layout.Margin(l=0,r=0, b=0, t=0), title=secim, paper_bgcolor="rgba(0,0,0,0)" ) # paper_bgcolor=' #0000b3 # templates=["ggplot2", "saborn", "plotly", plotly_dark ]
    

    return fig


### !!! PAGE UNDER CONSTRUCTION !!! ####
set_bg("./media/bg.jpg")
st.header("Türkiye Lisansüstü Çalışmaları\n Bağlam Haritası") 
database = st.sidebar.radio("Veri Tabanı Seçiniz", options= [ "Din" , "Felsefe"])

with open ( "README.md", "r" ) as f:
    txt = f.read()
    st.sidebar.text_area( label= "Tanıtım:", value= txt, height= 500, disabled= True )

matrix, kelime_listesi, main_df = matrix_reader(database.lower()) # din veya felsefe

st.markdown("___")
sec = st.selectbox(label="Kavram Seçiniz", options=kelime_listesi, index=2505, format_func= str.capitalize,  )
sec = Searcher(sec, main_df)

with st.expander( label="Detaylı Arama", expanded= False ) :
    col1, col2, col3, col4 = st.columns(4)

    yillar          = st.select_slider(label= "Yıl Aralığı Seç", options= sec.year_list, value=( min(sec.year_list), max(sec.year_list)) )
    danisman_filtre = col1.selectbox  (label= "Danışman Ara",    options= ["Tümü"] + list(set(sec.word_df.danisman.values.tolist() )),       index = 0 )
    yer_filtre      = col2.selectbox  (label= "Üniversite Ara",  options= ["Tümü"] + list(set(sec.word_df["yer bilgisi"].values.tolist() )), index = 0 )
    tur_filtre      = col3.selectbox  (label= "Tür Ara",         options= ["Tümü"] + list(set(sec.word_df.tur.values.tolist() )),            index = 0 )
    yazar_filtre    = col4.selectbox  (label= "Yazar Ara",       options= ["Tümü"] + list(set(sec.word_df.yazar.values.tolist() )),          index = 0 )

    col1, col2, col3, col4 = st.columns(4)
    filtered = col1.button("Filtreleri Uygula")
    reset_button = col4.button("Temizle")
    
    if filtered:
        filtered_df = sec.filter_callback(yil= yillar, yazar= yazar_filtre, danisman=danisman_filtre, yer_bilgisi=yer_filtre)
        sec.update(filtered_df)
        st.write(len(sec.word_df))
    elif reset_button:
        sec.update(main_df)
        st.write(len(sec.word_df))

st.markdown("___ ")

st.plotly_chart( express( sec.word ) )

st.markdown("___")

st.dataframe( sec.word_df )