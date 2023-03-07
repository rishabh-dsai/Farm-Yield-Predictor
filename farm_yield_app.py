# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 18:59:26 2023

@author: asus
"""

import streamlit as st
import joblib
import numpy as np
import pandas as pd


st.set_page_config(page_title='Farm Yield Prediction Model')

model=joblib.load("Farm Yield.sav")
soil_df=pd.read_excel("Agri Factor Master Sheet.xlsx")
env_df=pd.read_excel("Agri Factor Master Sheet.xlsx",sheet_name="Climate")

season_dict={'Maize':"Rabi",'Paddy':"Kharif",'Sugarcane':"Kharif", 'Wheat':"Rabi" }

#%%

# Header Display
st.markdown('<div style="text-align: center; font-size:30px; font-weight:bold">DSAI Digital Agriculture Platform</div>', unsafe_allow_html=True)
st.markdown("<br></br>",unsafe_allow_html=True)
st.markdown('<div style="background-color:orange;padding:10px"> <h2 style="color:white;text-align:center;">Farm Yield</h2> </div>',unsafe_allow_html=True)
st.markdown("<br></br>",unsafe_allow_html=True)

# Take Inputs
crop=st.selectbox("Crop",['Maize','Paddy','Sugarcane', 'Wheat' ])
district=st.selectbox("District",("Dehradun", "Champawat"),disabled=True)
block=st.selectbox("Block",("Vikasnagar", "Dalu"),disabled=True)
village=st.selectbox("Village",soil_df['Village Name'].unique())
farm=st.selectbox("Farm Number",soil_df.groupby('Village Name')['Farm Number'].unique()[village])
farm_size=st.number_input("Farm size (in hectare)",step=2)
season=season_dict[crop]

# ['Area', 'Humidity', 'K', 'N', 'P', 'Precipitation', 'Temperature',
#        'Crop Name_Maize', 'Crop Name_Paddy', 'Crop Name_Sugarcane',
#        'Crop Name_Wheat']

if st.button("Calculate"):
    inp_df=soil_df.set_index(['Village Name','Farm Number'])
    n=inp_df.loc[(village,farm),'N']
    p=inp_df.loc[(village,farm),'P']
    k=inp_df.loc[(village,farm),'K']
    
    inp_df_2=env_df.set_index(['Village Name','Season'])
    rain=inp_df_2.loc[(village,season),'Rainfall (Average in mm)']    
    temp=inp_df_2.loc[(village,season),'Temperature']
    humid=inp_df_2.loc[(village,season),'Humidity']
    crop_enc=[0,0,0,1]
    if crop=="Maize":
        crop_enc=[1,0,0,0]
    elif crop=="Paddy":
        crop_enc=[0,1,0,0]
    elif crop=="Sugarcane":
        crop_enc=[0,0,1,0]    
    inp_x=np.append([farm_size,humid,k,n,p,rain,temp],crop_enc)
    farm_yield=np.round(model.predict([inp_x])[0],2)
    farm_yield_op=np.round(farm_yield/farm_size,2)
    season_text="Season - "+season
    st.text(season_text)
    st.caption("Note - Soil health and nutirents as well as the weather parameters are taken into account.") 
#    string=("Crop Yield (in kg/ha)"+" - "+str(farm_yield_op)).upper()
    string_2=("Crop Yield (in kg/ha)"+" - "+str(farm_yield)).upper()
#    st.text(string)
    st.text(string_2)

















