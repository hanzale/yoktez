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
    
    with open("./database/%s_duzenli_dataframe.pickle"%alan , "rb") as f:
        df = pd.read_pickle(f)
    
    return co_occurrence_matrix, dizin_kelimeler, df



def set_bg(img):
 
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