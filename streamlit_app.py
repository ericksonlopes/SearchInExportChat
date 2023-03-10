import streamlit as st

from src.clear_file import BaseClearDataFile

data = st.file_uploader('Escolha o dataset (.csv)', type='csv')

base = BaseClearDataFile(file_data=data)

st.write(base.messages)