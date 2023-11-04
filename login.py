"""
Version élève sans authentification 
Permet d'accéder aux questions et aux réponses identification
Les url des google sheets ne sont modifiables que dans le code pas d'interface comme dans le mode enseignant
"""
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import random
import os
# ajout pour récupérer feuille ods
#import pyexcel as pe
#import requests

# Dictionnaire avec les url des 3 feuilles Google Sheets contenant les questions reponses
dico_url= {'classe_0': 'Teminale Spécialité', 'url0': 'https://docs.google.com/spreadsheets/d/1oBDNWpHnWua6n7UsoR0EEC_ecA1Y7hNs8KJ9u-6TLH8/edit#gid=0', 'classe_1': '1ère NSI', 'url1': 'https://docs.google.com/spreadsheets/d/1oBDNWpHnWua6n7UsoR0EEC_ecA1Y7hNs8KJ9u-6TLH8/edit#gid=1306826686', 'classe_2': 'Seconde', 'url2': 'https://docs.google.com/spreadsheets/d/1oBDNWpHnWua6n7UsoR0EEC_ecA1Y7hNs8KJ9u-6TLH8/edit#gid=1235869407'}

# Fonction utilisée pour importer googlesheet
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

# Fonction qui renvoie la clé associée à une valeur du dictionnaire
def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

# try:
#     username= st.session_state['username']
#     dico_url = st.session_state['dico_url']
# except:
#     switch_page("login")
#st.write(f"user: {username} url: {url}")


#st.write(df)
####



def creation_sommaire(df):
    sommaire = {}
    for i, row in df.iterrows():
        start = i
        nom_chap = row.Chapitre
        if nom_chap not in sommaire:
            sommaire[nom_chap] = [start, start]
        else: 
            sommaire[nom_chap][1] = i
    return sommaire

st.markdown(f"# :control_knobs: Réglages")
classe = st.selectbox("Choisir votre Classe", (dico_url[f"classe_{i}"] for i in range(3)))
numero_classe = get_key_by_value(dico_url,classe)[-1] #dernier caractère
url = dico_url[f"url{numero_classe}"] 
df =load_data(url)
# création sommaire liste des chapitre avec index premiere et derniere question du chapitre
sommaire = creation_sommaire(df)
chap_courant = st.selectbox("Choisir le chapitre en cours d'apprentissage", (k for k in sommaire.keys()))
#st.write(chap_courant)
#st.write(sommaire[chap_courant][1])
st.markdown(f"Ce chapitre contient :red[{sommaire[chap_courant][1]+1-sommaire[chap_courant][0]}] questions")
nb_question_dans_chap_courant = sommaire[chap_courant][1]+1-sommaire[chap_courant][0]
question_chap_courant_max = st.slider('Progression dans le chapitre', 0, nb_question_dans_chap_courant,nb_question_dans_chap_courant//2)
nb_question_courant = st.slider('Nombre de questions à poser sur le chapitre en cours',min_value = 1,max_value=question_chap_courant_max,value=2)
nb_question = st.number_input('Nombre de questions sur le passé',min_value = 1,max_value=sommaire[chap_courant][1]-(nb_question_dans_chap_courant-question_chap_courant_max),value=1)

st.markdown("## :fire: Questions sur la leçon")
# Calcul des index des questions corrspondant au début et fin du chapitre sélectionné
start_index = sommaire[chap_courant][0]
end_index = sommaire[chap_courant][1]
#st.write(start_index)
#st.write(end_index)
# Extraction des nb_question_courant
random_indexes_courant = random.sample(range(start_index,start_index+question_chap_courant_max), nb_question_courant)
#st.write(random_indexes_courant)
resultat_courant = df.iloc[random_indexes_courant]
# Extraction des nb_question
if start_index != 0:
    random_indexes = random.sample(range(0,start_index), nb_question)
else: 
    random_indexes=[]
resultat = df.iloc[random_indexes]

#for index, row in df.loc[start_index: end_index].iterrows():
for row in resultat_courant.itertuples():
    st.markdown(f"#### {row.Question}")
    st.divider()
#    st.markdown(f" {row['Question']} ")


st.markdown("## :calendar: Questions depuis le début de l'année")


for row in resultat.itertuples():
    st.markdown(f"#### {row.Question}")
    st.divider()

st.markdown("## Correction")
# Enregistrements des questions/reponses dans la session
st.session_state['resultat_courant']=resultat_courant
st.session_state['resultat']=resultat
#st.session_state['username']=username

with st.expander("Afficher"):
    st.markdown(f"### :fire:")
    for row in resultat_courant.itertuples():
        st.markdown(f"##### **{row.Question}**  ")
        st.markdown(f"- #### {row.Answer}")
        st.divider()

    st.markdown(f"### :date:")
    for row in resultat.itertuples():
        st.markdown(f"##### **{row.Question}** ")
        st.markdown(f"- #### {row.Answer}")
        st.divider()