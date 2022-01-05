# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 17:49:57 2022

@author: ty-kim
"""
import streamlit as st
import pandas as pd
import sqlalchemy

st.title('Fundamentals comparison')

engine = sqlalchemy.create_engine('sqlite:///D:/Fundamentals.db')

# symbol column을 index로 사용
df = pd.read_sql('Fundamentalstable', engine, index_col=['symbol'])

dropdownI = st.selectbox('Choose your sector', df.sector.unique())

dropdownII = st.selectbox('Choose your metric', df.columns[df.columns != 'sector'])

values = df[df.sector == dropdownI][[dropdownII]]

st.bar_chart(values)