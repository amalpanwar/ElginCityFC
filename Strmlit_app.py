#!/usr/bin/env python
# coding: utf-8
import subprocess
import sys

import numpy as np
# from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
# from langchain_community.vectorstores import Milvus
# from langchain_qdrant import QdrantVectorStore
# from qdrant_client import QdrantClient
# from langchain_community.vectorstores import Qdrant
import matplotlib.pyplot as plt
# import mplcursors
import seaborn as sns
from scipy.stats import norm
from math import pi
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import sqlite3
#from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, AIMessage
import getpass
import os
# from dotenv import load_dotenv
from langchain import hub
# import chromadb
# from langchain.vectorstores import Chroma
# from langchain_community.vectorstores import Chroma
# from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from chromadb import Chroma
# from langchain_chroma import Chroma
#from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
#from langchain_openai import OpenAIEmbeddings
#from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceHubEmbeddings
# from langchain_mistralai import ChatMistralAI
# from langchain_together import ChatTogether
from langchain_ai21 import ChatAI21
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_community.vectorstores import Qdrant
# from langchain_deepseek import ChatDeepSeek
#from unstructured.partition.xlsx import partition_xlsx
import networkx as nx
#import pandas as pd
import json
import bs4
import base64
#from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import CSVLoader
# from langchain.document_loaders import CSVLoader
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import logging
# import chromadb
# import chromadb.config

logging.basicConfig(level=logging.DEBUG)
#import sqlite3

# import subprocess
import streamlit as st

# def check_qdrant():
#     try:
#         import qdrant_client
#         st.write("✅ Qdrant-client is installed")
#     except ModuleNotFoundError:
#         st.write("❌ Qdrant-client is NOT installed")

# st.write("Checking installed packages...")
# installed_packages = subprocess.run(["pip", "list"], capture_output=True, text=True)
# st.text(installed_packages.stdout)

# check_qdrant()


# ******************* Data Loading **************************************
# df = pd.read_excel("CM_Elgin.xlsx")
df_CM = pd.read_csv("CM_ElginFC.csv",encoding='ISO-8859-1')
df_CB = pd.read_csv("CB_ElginFC.csv",encoding='ISO-8859-1')
df_Wing = pd.read_csv("Wing_ElginFC.csv",encoding='ISO-8859-1')
df_CF=pd.read_csv("CF_ElginFC.csv",encoding='ISO-8859-1')
df_GK=pd.read_csv("GK_ElginFC.csv",encoding='ISO-8859-1')
df_FB=pd.read_csv("FB_ElginFC.csv",encoding='ISO-8859-1')
df_CAM=pd.read_csv("CAM_ElginFC.csv",encoding='ISO-8859-1')

pvt_df_CM = pd.DataFrame(df_CM).set_index('Player')
df_CB[df_CB.columns[3:]] = df_CB[df_CB.columns[3:]].apply(pd.to_numeric, errors='coerce').fillna(0)
pvt_df_CB = pd.DataFrame(df_CB).set_index('Player')
pvt_df_Wing = pd.DataFrame(df_Wing).set_index('Player')
df_CF[df_CF.columns[3:]] = df_CF[df_CF.columns[3:]].apply(pd.to_numeric, errors='coerce')
pvt_df_CF = pd.DataFrame(df_CF).set_index('Player')
df_GK[df_GK.columns[3:]] = df_GK[df_GK.columns[3:]].apply(pd.to_numeric, errors='coerce').dropna()
pvt_df_GK = pd.DataFrame(df_GK).set_index('Player')
pvt_df_FB = pd.DataFrame(df_FB).set_index('Player')
df_CAM[df_CAM.columns[3:]] = df_CAM[df_CAM.columns[3:]].apply(pd.to_numeric, errors='coerce')
pvt_df_CAM = pd.DataFrame(df_CAM).set_index('Player')

#******************************* background image setting *******************************************************************
def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        image_bytes = file.read()
        base64_image = base64.b64encode(image_bytes).decode()
    return base64_image

# Get base64 version of your image
image_base64 = get_base64_image("image/soccerplayer2.webp")

# Add the base64 image to the background using CSS
background_image = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{image_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)


st.markdown(
    """
    <style>
    .css-1d391kg {
        width: 200px;  /* Adjust the width of the sidebar */
    }
    .css-1d391kg .css-e1fqkh5 {
        width: 800px;  /* Adjust the width of the inner content */
    }
    </style>
    """,
    unsafe_allow_html=True
    )

#Logo
image_logo = get_base64_image("image/Elgin_City_FC_Badge.png")
# logo_url = "image/Elgin_City_FC_Badge.png"  # Replace with your logo URL

# Inject CSS to place the logo in the top-right corner
st.markdown(
    f"""
    <style>
    .logo {{
        position: fixed;
        top: 70px;
        right: 10px;
        width: 120px;  /* Adjust the size */
    }}
    </style>
    <img src="data:image/png;base64,{image_logo}" class="logo">
    """,
    unsafe_allow_html=True
)

##*********************** Radar Chart ***************************************************************************************
def create_radar_chart(df, players, id_column, title=None, max_values=None, padding=1.25):
    # Select data for the chosen players
    df_selected = df.loc[players]
    categories = df_selected.columns.tolist()
    data = df_selected.to_dict(orient='list')
    ids = df_selected.index.tolist()

    # Determine if there are any negative values
    has_negative_values = any(min(value) < 0 for value in data.values())

    # Define max values for normalization (handling both positive and negative values)
    if max_values is None:
        max_values = {key: padding * max(np.abs(value)) for key, value in data.items()}  # Use absolute max for both positive and negative values
    else:
        for key, max_val in max_values.items():
            if max_val == 0 or np.isnan(max_val):
                max_values[key] = padding * max(np.abs(data[key]))  # Ensure to account for negative values too

    # Normalize data based on max_values
    normalized_data = {}
    for key, value in data.items():
        normalized_data[key] = np.array(value) / max_values[key]  # Normalize all values

    # Create radar chart using Plotly
    fig = go.Figure()

    for i, model_name in enumerate(ids):
        values = [normalized_data[key][i] for key in data.keys()]
        values += values[:1]  # Complete the circle

        hovertext = [f"{categories[j]}: {data[c][i]:.2f}" for j, c in enumerate(categories)]
        hovertext += [hovertext[0]]  # Complete the circle for hovertext

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            name=model_name,
            hoverinfo='text',
            hovertext=hovertext
        ))

    # Determine the radial axis range dynamically
    radial_range = [-1, 1] if has_negative_values else [0, 1]

    # Customize layout with dynamic radial axis range
    fig.update_traces(
        hoverlabel=dict(
            bgcolor='white',  # Background color of the hover label
            font=dict(
                color='black'  # Text color of the hover label
            )
        )
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=radial_range,  # Dynamic range: [-1, 1] for negative values, [0, 1] otherwise
                showticklabels=False,
                # tickvals=[-1, -0.5, 0, 0.5, 1] if has_negative_values else [0, 0.5, 1],  # Adjust ticks based on the range
                # ticktext=['-1', '-0.5', '0', '0.5', '1'] if has_negative_values else ['0', '0.5', '1'],
                showline=False,
                ticks="",
                showgrid=True,
                gridcolor='gray',
                gridwidth=1,
            ),
            angularaxis=dict(
                tickvals=list(range(len(categories))),
                ticktext=categories + [categories[0]],
                rotation=0,
                direction="clockwise",
                showticklabels=True,
                showline=True,
                showgrid=True,
                gridcolor='gray',
                gridwidth=1,
                tickfont=dict(size=9.5, color='white'),
            ),
        ),
        title=dict(
            text=title,
            font=dict(size=12)
        ),
        width=1000,  # Increased width for better clarity
        height=300,  # Increased height for better clarity
        margin=dict(l=100, r=100, t=20, b=20),
        paper_bgcolor='black',  # Background color
        plot_bgcolor='white',   # Plot area background color
        legend=dict(
            orientation="v",  # Horizontal orientation
            yanchor="bottom",
            y=-0.1, 
            xanchor="right",
            x=0.08,
            bgcolor='white',
            bordercolor='white',
            borderwidth=1,
            font=dict(size=10, color='black')
        )
    )

    return fig

##*********************** Guage Chart ***************************************************************************************
def create_gauge_chart(player_name, rating, rank, age, team, matches_played, minutes_played,Position,league_average_rating):
    # Format the title text with HTML to include additional information
    title_text = f"""
    <span style="font-size:16px"><b>{player_name}</b></span><br>
    <span style="font-size:12px">Rank: {rank}</span><br>
    <span style="font-size:10px">Team: {team}</span><br>
    <span style="font-size:10px">Age: {age} | Matches: {matches_played} | Minutes: {minutes_played}</span><br>
    <span style="font-size:10px"><b>{Position}</b></span>
    """
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=rating,
        delta={'reference': league_average_rating, 'increasing': {'color': 'green'}, 'decreasing': {'color': 'red'}}, 
        number={'valueformat': '.2f'},
        title={'text': title_text, 'font': {'size': 16}},  # Reduce the font size
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
        }
    ))
    # Adjust layout to handle the extra text and space
    fig.update_layout(
        height=350,  # Adjust height to accommodate more text
        width=300, 
        margin=dict(t=50, b=0, l=0, r=0)  # Top margin to give space for title
    )
    return fig


#****************************************************** Zscore *************************************************
def standardize_and_score_football_metrics(df, metrics, weights=None):
    # Automatically categorize metrics
    percent_metrics = [col for col in metrics if '%' in col]
    per90_metrics = [col for col in metrics if col not in percent_metrics]
    
    # If weights are not provided, use equal weights
    if weights is None:
        weights = [1] * len(metrics)
    
    # Ensure weights match the number of metrics
    assert len(metrics) == len(weights), "Number of metrics and weights must match"
    
    # Function to calculate distance from 50% for percentage metrics
    def distance_from_50(x):
        return abs(x - 50) / 50  # Normalized distance from 50%
    
    # Standardize and weight metrics
    standardized_metrics = pd.DataFrame()
    for metric, weight in zip(metrics, weights):
        if metric in percent_metrics:
            standardized_metrics[metric] = df[metric].apply(distance_from_50) * weight
        else:  # per90 metrics
            mean = df[metric].mean()
            std = df[metric].std()
            standardized_metrics[metric] = ((df[metric] - mean) / std) * weight
    
    # Aggregate the score final score
    df["Score"] = standardized_metrics.mean(axis=1)
    
    # Calculate final z-score
    original_mean = df["Score"].mean()
    original_std = df["Score"].std()
    df["Score"] = (df["Score"] - original_mean) / original_std
    
    # Calculate final score (0-100)
    df["Score(0-100)"] = (norm.cdf(df["Score"]) * 100).round(2)
    
    # Calculate player rank
    df['Rank'] = df['Score(0-100)'].rank(ascending=False)
    
    return df




# Streamlit app

# ******************* RAG Pipeline for Chatting ********************************
# def initialize_rag(csv_file, llm_api_key=st.sidebar.text_input('LLM API Key'), api_token=st.sidebar.text_input('API Key', type='password')):
#     if not llm_api_key or not api_token:
#         st.error("Please provide both the LLM API Key and the API Key.")
#         return
    
#     try:
#         # Initialize the LLM model
#         llm = ChatAI21(
#             model="jamba-1.5-large",
#             api_key=llm_api_key,
#             max_tokens=4096,
#             temprature=0.1,
#             top_p=1,
#             stop=[]
#         )
        
#         # Load document through CSVLoader
#         loader = CSVLoader(csv_file, encoding="windows-1252")
#         docs = loader.load()
        
#         # Initialize HuggingFaceHubEmbeddings with the provided API token
#         embeddings = HuggingFaceHubEmbeddings(huggingfacehub_api_token=api_token)
        
#         # Initialize FAISS vector store
#         try:
            
#             vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)
#             retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 20, 'fetch_k': 20})
#         except Exception as e:
#             logging.error(f"Error initializing FAISS vector store: {str(e)}")
#             return
        
#         # Preparing Prompt for Q/A
#         system_prompt = (
#             "You are an assistant for question-answering tasks. "
#             "Use the following pieces of retrieved context to answer "
#             "the question. If you don't know the answer, say that you "
#             "don't know. Use three sentences minimum and keep the "
#             "answer concise."
#             "\n\n"
#             "{context}"
#         )
        
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", system_prompt),
#             ("human", "{input}")
#         ])
        
#         question_answer_chain = create_stuff_documents_chain(llm, prompt)
#         rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
#         user_prompt = st.text_input("Enter your query:")
#         if user_prompt:
#             response = rag_chain.invoke({"input": user_prompt})
#             st.write(response["answer"])
        
#     except Exception as e:
#         logging.error(f"Error: {str(e)}")

llm_api_key = st.sidebar.text_input('Together API Key')
api_token = st.sidebar.text_input('API Key', type='password')

logging.basicConfig(level=logging.DEBUG)

# def initialize_rag(csv_file, llm_api_key=st.sidebar.text_input('LLM API Key'), api_token=st.sidebar.text_input('API Key', type='password')):
#     if not llm_api_key or not api_token:
#         st.error("Please provide both the LLM API Key and the API Key.")
#         logging.error("Missing API keys: LLM API Key or API Key not provided.")
#         return

#     try:
#         logging.info("🔹 Connecting to Milvus...")
#         connections.connect(alias="default", host="172.18.0.4", port="19530")
#         logging.info("✅ Successfully connected to Milvus!")

#         # Initialize LLM Model
#         logging.info("🔹 Initializing LLM Model (Jamba-1.5-Large)...")
#         llm = ChatAI21(
#             model_name="jamba-1.5-large",
#             openai_api_key=llm_api_key,
#             temperature=0.1,
#             max_tokens=4096
#         )
#         logging.info("✅ LLM Model initialized successfully!")

#         # Load documents from CSV
#         logging.info(f"🔹 Loading CSV file: {csv_file}")
#         loader = CSVLoader(csv_file, encoding="windows-1252")
#         docs = loader.load()
#         logging.info(f"✅ Successfully loaded {len(docs)} documents from CSV!")

#         # Initialize HuggingFace Embeddings
#         logging.info("🔹 Initializing HuggingFace Embeddings...")
#         embeddings = HuggingFaceEmbeddings()
#         logging.info("✅ HuggingFace Embeddings initialized successfully!")

#         # Define collection name
#         collection_name = "documents"

#         # Initialize Milvus vector store
#         logging.info(f"🔹 Initializing Milvus vector store with collection: {collection_name}...")
#         vectorstore = Milvus(
#             embedding_function=embeddings,
#             collection_name=collection_name,
#             connection_args={"host": "172.18.0.4", "port": "19530"}
#         )
#         logging.info("✅ Milvus vector store initialized!")

#         # Insert documents into Milvus
#         logging.info("🔹 Inserting documents into Milvus...")
#         vectorstore.add_documents(docs)
#         logging.info("✅ Documents successfully inserted into Milvus!")

#         # Create retriever
#         logging.info("🔹 Creating retriever from Milvus vector store...")
#         retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={'k': 20})
#         logging.info("✅ Retriever created successfully!")

#         # Define prompt
#         logging.info("🔹 Setting up system prompt...")
#         system_prompt = (
#             "You are an assistant for question-answering tasks. "
#             "Use the following pieces of retrieved context to answer "
#             "the question. If you don't know the answer, say that you don't know."
#             "Use three sentences minimum and keep the answer concise."
#             "\n\n"
#             "{context}"
#         )
#         logging.info("✅ System prompt set!")

#         prompt = ChatPromptTemplate.from_messages([
#             ("system", system_prompt),
#             ("human", "{input}")
#         ])

#         # Create chains
#         logging.info("🔹 Creating document retrieval and question-answering chains...")
#         question_answer_chain = create_stuff_documents_chain(llm, prompt)
#         rag_chain = create_retrieval_chain(retriever, question_answer_chain)
#         logging.info("✅ Chains created successfully!")

#         # User input
#         user_prompt = st.text_input("Enter your query:")
#         if user_prompt:
#             logging.info(f"🔹 Received user query: {user_prompt}")
#             response = rag_chain.invoke({"input": user_prompt})
#             logging.info("✅ Response generated successfully!")
#             st.write(response["answer"])

#     except Exception as e:
#         logging.error(f"❌ Error in #initialize_rag: {str(e)}")
#         st.error(f"An error occurred: {str(e)}")
#  ****************** Title ****************************
st.title('Player Performance Dashboard')

# ******************* Position selection ********************************************************
default_position_index = ["GK","FB","CB","CM","CAM","Winger","CF"].index('CM')
position = st.sidebar.selectbox('Select position:', options=["GK","FB","CB","CM","CAM","Winger","CF"],index=default_position_index)





# Ensure df_position is selected
##******************************** CM  - Center Midfielder **************************************************************************
if position == 'CM':
    df_position = pvt_df_CM

    # Assign weights to the metrics based on their importance
    original_metrics =[
       'Assists per 90',
       'Successful defensive actions per 90', 'Aerial duels won per 90', 'Interceptions per 90', 'Fouls per 90',
       'Shots on target per 90', 'Accurate passes per 90',
       'Accurate forward passes per 90', 'Key passes per 90']
    weights=[1,1,0.9,1,-1.25,1,0.9,1,1.25]
    #weighted_metrics = pd.DataFrame()
    df_position['Assists per 90'] = ((df_position['Assists'] / df_position['Minutes played']) * 90).round(2)
    df_position['Aerial duels won per 90'] = df_position['Aerial duels per 90'] * (df_position['Aerial duels won, %'] / 100)
    df_position['Accurate passes per 90'] = df_position['Passes per 90'] * (df_position['Accurate passes, %'] / 100)
    df_position['Accurate forward passes per 90'] = df_position['Forward passes per 90'] * (df_position['Accurate forward passes, %'] / 100)
    df_position['Shots on target per 90'] = df_position['Shots per 90'] * (df_position['Shots on target, %'] / 100)
    #df_position['Accurate passes to final third per 90'] = df_position['Passes to final third per 90'] * (df_position['Accurate passes to final third, %'] / 100)
   
    df_position = standardize_and_score_football_metrics(df_position, original_metrics, weights)

    # Dropdown menu for player selection based on position
    if st.sidebar.button('Show Top 5 Players'):
        top_5_players = df_position.nsmallest(5, 'Rank').index.tolist()
    # Multiselect only includes top 5 players
        players_CM = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
    else:
    # Multiselect includes all players
        players_CM = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])

    # players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_CM]

    
    df_filtered_new=df_position.reset_index()
    league_avg_row = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']

# Extract league average values
    league_avg_values = {
    'Passes per 90': league_avg_row['Passes per 90'].values[0],
    'Forward passes per 90': league_avg_row['Forward passes per 90'].values[0],
    'Key passes per 90': league_avg_row['Key passes per 90'].values[0],
    #'Passes to final third per 90': league_avg_row['Passes to final third per 90'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Passes per 90'].max()
    y_max_values = {
    'Forward passes per 90': df_filtered_new['Forward passes per 90'].max(),
    'Key passes per 90': df_filtered_new['Key passes per 90'].max(),
    #'Passes to final third per 90': df_filtered_new['Passes to final third per 90'].max()
           }
    # y_max = max(y_max_values.values())
   
    # create Scatter plot
    fig = px.scatter(df_filtered.reset_index(), x='Passes per 90', y=[ 'Forward passes per 90','Key passes per 90'], facet_col='variable',
                                facet_col_spacing=0.08, color='Player',title='Passing threats')
    
    

# Add horizontal and vertical lines for each facet, this will provide the quadrant inside scatter plot
    
    for i, facet_name in enumerate(['Forward passes per 90', 'Key passes per 90']):
        # Add horizontal line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=0,
            y0=league_avg_values[facet_name],
            x1=x_max,
            y1=league_avg_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='red', width=1, dash='dash')
              )
          
           )

    # Add vertical line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=league_avg_values['Passes per 90'],
            y0=0,
            x1=league_avg_values['Passes per 90'],
            y1=y_max_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='blue', width=1, dash='dash')
             )
              
              )

    fig.update_traces(textposition='top center')
    fig.update_traces(marker=dict(size=8))
    fig.update_yaxes(matches=None)
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    for annotation in fig.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig)
    
   # Dropping unnecessary column not require for radar chart
    df_position2=df_filtered.drop(columns=['Score(0-100)', 'Position','Score','Rank','Age','Team', 'Matches played', 'Minutes played',
                                          'Assists','Aerial duels per 90','Aerial duels won, %', 'Passes per 90','Accurate passes, %', 'Forward passes per 90',
                                          'Accurate forward passes, %','Shots on target per 90', 'Shots per 90'])

    # Radar chart
    radar_fig =create_radar_chart(df_position2, players_CM, id_column='Player', title=f'Radar Chart for {position} (Default: League Average)')
    st.plotly_chart(radar_fig)
   
    # Gauge Chart
    st.write("Player Ratings Gauge Chart")
    df_filtered_guage=df_filtered.reset_index()
    league_average_rating = df_filtered_new.loc[df_filtered_new['Player'] == 'League Two Average', 'Score(0-100)'].values[0]
    players = df_filtered_guage['Player'].tolist()
    ratings = df_filtered_guage['Score(0-100)'].tolist()
    ranks = df_filtered_guage['Rank'].tolist()
    Age = df_filtered_guage['Age'].tolist()
    Team = df_filtered_guage['Team'].tolist()
    Matches=df_filtered_guage['Matches played'].tolist()
    Minutes=df_filtered_guage['Minutes played'].tolist()
    Position=df_filtered_guage['Position'].tolist()

    for i in range(0, len(players), 3):  # 3 charts per row
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(players):
                with cols[j]:
                    fig = create_gauge_chart(players[i + j], ratings[i + j], ranks[i + j],Age[i + j], Team[i + j], Matches[i + j], Minutes[i + j],Position[i + j],league_average_rating)
                    st.plotly_chart(fig)


        
   # Calculating Assit per 90 for slected player and for league average 
    df_filtered2 = df_filtered.reset_index()
    league_avg_row2 = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']
    league_avg_values2 = {
    'Key passes per 90': league_avg_row2['Key passes per 90'].values[0],
    'Assists per 90': league_avg_row2['Assists per 90'].values[0],
    'Interceptions per 90': league_avg_row2['Interceptions per 90'].values[0],
          }

    # calculate min, max for the quadrants
    x_min, x_max = df_filtered_new['Key passes per 90'].min(), df_filtered_new['Key passes per 90'].max()
    y_min, y_max = df_filtered_new['Assists per 90'].min(), df_filtered_new['Assists per 90'].max()
    y_min_int, y_max_int = df_filtered_new['Interceptions per 90'].min(), df_filtered_new['Interceptions per 90'].max()

    # creating scatter plot
    fig2 = px.scatter(df_filtered2, x='Key passes per 90',y='Assists per 90',
                     color='Player', title=f'{position} Progression ability')
    # Adding quadrants
    fig2.add_shape(
    go.layout.Shape(
        type='line',
        x0=x_min,
        y0=league_avg_values2['Assists per 90'], 
        x1=x_max,
        y1=league_avg_values2['Assists per 90'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             )
             )

    fig2.add_shape(
    go.layout.Shape(
        type='line',
        x0=league_avg_values2['Key passes per 90'], 
        y0=y_min,
        x1=league_avg_values2['Key passes per 90'],
        y1=y_max,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              )
           )
  
    fig2.update_traces(textposition='top center')
    fig2.update_traces(marker=dict(size=8))
#Create scatter plot
    fig22 = px.scatter(df_filtered2, x='Key passes per 90',y='Interceptions per 90',
                     color='Player', title=f'{position} Attack vs Defensive ability')
    # Add quadrants
    fig22.add_shape(
    go.layout.Shape(
        type='line',
        x0=x_min,
        y0=league_avg_values2['Interceptions per 90'], 
        x1=x_max,
        y1=league_avg_values2['Interceptions per 90'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             )
             )

    fig22.add_shape(
    go.layout.Shape(
        type='line',
        x0=league_avg_values2['Key passes per 90'], 
        y0=y_min_int,
        x1=league_avg_values2['Key passes per 90'],
        y1=y_max_int,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              )
           )
  
    fig22.update_traces(textposition='top center')
    fig22.update_traces(marker=dict(size=8))
    col1, col2 = st.columns([1, 1])
    # display visuals 
    with col1:
        st.plotly_chart(fig2)
    with col2:
        st.plotly_chart(fig22)
    

 # sort the vlaues by Aerial duel per 90 CM involved.
    df_filtered3 = df_filtered2.sort_values(by='Aerial duels won per 90', ascending=False)
    # max_aerial_duels_won = df_filtered_new['Aerial duels won per 90'].max()
    
    fig3 = px.bar(
    df_filtered3, 
    x='Aerial duels won per 90', 
    y='Player', 
    orientation='h', 
    title=f'{position} Aerial wining ability',
    color='Aerial duels won per 90',  # Color based on 'Aerial duels won per 90'
    color_continuous_scale='oranges'  # Color scale from dark to light
    # range_color=[0, max_aerial_duels_won]    
         )

# Reverse the color scale so that higher values are darker
    fig3.update_layout(coloraxis_colorbar=dict(title="Aerial duels won per 90"))
    st.plotly_chart(fig3)
    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get API Keys from UI
    # llm_api_key = st.sidebar.text_input("LLM API Key")
    # api_token = st.sidebar.text_input("API Key", type="password")

    if not llm_api_key or not api_token:
         st.error("Please provide both the LLM API Key and the API Key.")
         logging.error("API Keys are missing.")
    else:
        try:
        # Initialize the LLM model
            logging.info("Initializing LLM model...")
            llm = ChatAI21(
            model="jamba-instruct-preview",
            api_key=llm_api_key,
            max_tokens=4096,
            temperature=0.1,  # Fixed typo from `temprature` to `temperature`
            top_p=1,
            stop=[],
              )
            logging.info("LLM model initialized successfully.")

        # Verify that the CSV file exists
            csv_file = "CM_ElginFC.csv"
            if not os.path.exists(csv_file):
                logging.error(f"CSV file not found: {csv_file}")
                st.error(f"CSV file not found: {csv_file}")
            else:
            # Loading document through loader
                logging.info(f"Loading document: {csv_file}")
                loader = CSVLoader(csv_file, encoding="windows-1252")
                docs = loader.load()
                logging.info(f"Documents loaded successfully. Found {len(docs)} documents.")

            # Initialize HuggingFaceHubEmbeddings with the provided API token
                logging.info("Initializing HuggingFaceHubEmbeddings...")
                embedding = HuggingFaceHubEmbeddings(huggingfacehub_api_token=api_token)
                logging.info("HuggingFaceHubEmbeddings initialized successfully.")

            # Initialize FAISS vector store
                try:
                    logging.info("Initializing Qdrant vector store...")
                    client = QdrantClient(url="http://127.0.0.1:6333")  # Use in-memory Qdrant for testing. Change to a real endpoint for production.

                # Create collection if not exists
                    collection_name = "elgin_fc"
                    client.recreate_collection(
                         collection_name=collection_name,
                         vectors_config=VectorParams(size=768, distance=Distance.COSINE),  # Adjust size according to the embedding model
                              )
                    logging.info(f"Qdrant collection '{collection_name}' initialized.")

                # Load documents into Qdrant
                    vectorstore = Qdrant.from_documents(
                         documents=docs,
                         embedding=embedding,
                         collection_name=collection_name,
                           )
                    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 20, 'fetch_k': 20})
                    logging.info("FAISS vector store initialized successfully.")

                # Preparing Prompt for Q/A
                    system_prompt = (
                    "You are an assistant for question-answering tasks. "
                    "Use the following pieces of retrieved context to answer "
                    "the question. If you don't know the answer, say that you "
                    "don't know. Use three sentences minimum and keep the "
                    "answer concise."
                    "\n\n"
                    "{context}"
                     )

                    prompt = ChatPromptTemplate.from_messages([
                       ("system", system_prompt),
                       ("human", "{input}"),
                       ])

                    logging.info("Initializing question-answer chain...")
                    question_answer_chain = create_stuff_documents_chain(llm, prompt)
                    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
                    logging.info("RAG chain initialized successfully.")

                # User input
                    user_prompt = st.text_input("Enter your query:")
                    if user_prompt:
                        logging.info(f"Processing user query: {user_prompt}")
                        response = rag_chain.invoke({"input": user_prompt})
                        st.write(response.get("answer", "No answer found."))
                        logging.info("Response generated successfully.")

                except Exception as e:
                    logging.error(f"Error initializing Qdrant vector store: {str(e)}")
                    st.error(f"Error initializing Qdrant vector store: {str(e)}")

        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            st.error(f"An error occurred: {str(e)}")
        
    
    
    # #initialize_rag('CM_ElginFC.csv')
    
    

###################################################### CB: Center Back #############################################    
elif position == 'CB':
    df_position = pvt_df_CB

    original_metrics =[
       'Successful defensive actions per 90', 'Defensive duels won per 90',
        'Aerial duels won per 90','PAdj Sliding tackles', 'Shots blocked per 90',
       'PAdj Interceptions', 'Fouls per 90', 'Accurate passes to final third/90','Accurate progressive passes/90']
    weights=[1,1.25,1,1,1,1,-1,0.8,0.8]
    weighted_metrics = pd.DataFrame()
    df_position['Aerial duels won per 90'] = df_position['Aerial duels per 90'] * (df_position['Aerial duels won, %'] / 100)
    df_position['Defensive duels won per 90'] = df_position['Defensive duels per 90'] * (df_position['Defensive duels won, %'] / 100)
    df_position['Accurate passes to final third/90'] = df_position['Passes to final third per 90'] * (df_position['Accurate passes to final third, %'] / 100)
    df_position['Accurate progressive passes/90'] = df_position['Progressive passes per 90'] * (df_position['Accurate progressive passes, %'] / 100)
    
    df_position = standardize_and_score_football_metrics(df_position, original_metrics, weights)

    if st.sidebar.button('Show Top 5 Players'):
        df_position_reset = df_position.reset_index()
        df_position_sorted = df_position_reset.sort_values(by='Score(0-100)', ascending=False)  # Assuming higher score is better

# Remove duplicates, keeping the one with the highest 'Defender Score(0-100)'
        df_position_unique = df_position_sorted.drop_duplicates(subset='Player', keep='first')

# Step 2: Get the top 5 players
        top_5_df = df_position_unique.head(5) 
        # Extract top 5 player names and their unique identifiers
        top_5_players = top_5_df[['Player', 'Score(0-100)']].set_index('Player').to_dict()['Score(0-100)']
        top_5_player_names = list(top_5_players.keys())
    
    # Multiselect only includes top 5 players
        players_CB = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
        df_filtered2 = df_position_reset[df_position_reset['Player'].isin(players_CB)]
    
    # To ensure only the best rank is retained for each player
        df_filtered2 = df_filtered2.sort_values(by='Score(0-100)', ascending=False)
        df_filtered2 = df_filtered2.drop_duplicates(subset='Player', keep='first')

    else:
    # Multiselect includes all players
        players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
        df_filtered = df_position.loc[players_CB]
        df_filtered2=df_filtered.reset_index()


    df_filtered_new=df_position.reset_index()
    league_avg_row = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']

# Extract league average values
    league_avg_values = {
    'Successful defensive actions per 90': league_avg_row['Successful defensive actions per 90'].values[0],
    'Shots blocked per 90': league_avg_row['Shots blocked per 90'].values[0],
    'PAdj Interceptions': league_avg_row['PAdj Interceptions'].values[0],
    'PAdj Sliding tackles': league_avg_row['PAdj Sliding tackles'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Successful defensive actions per 90'].max()
    y_max_values = {
    'Shots blocked per 90': df_filtered_new['Shots blocked per 90'].max(),
    'PAdj Interceptions': df_filtered_new['PAdj Interceptions'].max(),
    'PAdj Sliding tackles': df_filtered_new['PAdj Sliding tackles'].max()
           }
   

    df_filtered2 = df_filtered2.rename(columns={'Successful defensive actions per 90': 'Successful def. Action/90'})
   
    
    fig = px.scatter(df_filtered2, x='Successful def. Action/90', y=['Shots blocked per 90', 'PAdj Interceptions', 'PAdj Sliding tackles'], facet_col='variable',
                 facet_col_spacing=0.08, color='Player',  title='CB Defensive Actions')

    for i, facet_name in enumerate(['Shots blocked per 90', 'PAdj Interceptions', 'PAdj Sliding tackles']):
        # Add horizontal line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=0,
            y0=league_avg_values[facet_name],
            x1=x_max,
            y1=league_avg_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='red', width=1, dash='dash')
              )
          
           )

    # Add vertical line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=league_avg_values['Successful defensive actions per 90'],
            y0=0,
            x1=league_avg_values['Successful defensive actions per 90'],
            y1=y_max_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='blue', width=1, dash='dash')
             )
              
              )

    fig.update_traces(textposition='top center')
    fig.update_traces(marker=dict(size=8))
    fig.update_yaxes(matches=None)
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    for annotation in fig.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig)
  

    # Create radar chart for selected players
    df_position2=df_filtered2.drop(columns=[ 'Score','Score(0-100)','Rank','Team','Position','Age',
                        'Matches played','Minutes played','Defensive duels per 90', 'Defensive duels won, %',
       'Aerial duels per 90', 'Aerial duels won, %', 'Passes to final third per 90',
       'Accurate passes to final third, %', 'Progressive passes per 90',
       'Accurate progressive passes, %'])
                              
    radar_fig =create_radar_chart(df_position2.set_index('Player'), players_CB, id_column='Player', title=f'Radar Chart for Selected {position} (Default: League Average)')
    st.plotly_chart(radar_fig)
    # Create Guage chart for selected players
    st.write("Player Ratings Gauge Chart")
    df_filtered_guage=df_filtered2
    league_average_rating = df_filtered_new.loc[df_filtered_new['Player'] == 'League Two Average', 'Score(0-100)'].values[0]
    players = df_filtered_guage['Player'].tolist()
    ratings = df_filtered_guage['Score(0-100)'].tolist()
    ranks = df_filtered_guage['Rank'].tolist()
    Age = df_filtered_guage['Age'].tolist()
    Team = df_filtered_guage['Team'].tolist()
    Matches=df_filtered_guage['Matches played'].tolist()
    Minutes=df_filtered_guage['Minutes played'].tolist()
    Position=df_filtered_guage['Position'].tolist()

    for i in range(0, len(players), 3):  # 3 charts per row
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(players):
                with cols[j]:
                    fig = create_gauge_chart(players[i + j], ratings[i + j], ranks[i + j],Age[i + j], Team[i + j], Matches[i + j], Minutes[i + j],Position[i + j],league_average_rating)
                    st.plotly_chart(fig)



    # league_avg_row2 = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']
    league_avg_values2 = {
    'Defensive duels per 90': league_avg_row['Defensive duels per 90'].values[0],
    'Accurate passes to final third/90': league_avg_row['Accurate passes to final third/90'].values[0],
    'Accurate progressive passes/90': league_avg_row['Accurate progressive passes/90'].values[0],
    'Fouls per 90': league_avg_row['Fouls per 90'].values[0],
          }
    x_max = df_filtered_new['Defensive duels per 90'].max()
    y_max_values = {
    'Accurate passes to final third/90': df_filtered_new['Accurate passes to final third/90'].max(),
    'Accurate progressive passes/90': df_filtered_new['Accurate progressive passes/90'].max(),
    'Fouls per 90': df_filtered_new['Fouls per 90'].max()
           }
    y_min_values = {
    'Accurate passes to final third/90': df_filtered_new['Accurate passes to final third/90'].min(),
    'Accurate progressive passes/90': df_filtered_new['Accurate progressive passes/90'].min(),
    'Fouls per 90': df_filtered_new['Fouls per 90'].min()
           }

    fig2 = px.scatter(df_filtered2, x='Defensive duels per 90', y=['Accurate passes to final third/90','Accurate progressive passes/90','Fouls per 90'],facet_col='variable',
                 facet_col_spacing=0.08,color='Player', title=f'{position} with Progressive ability and Fouls Committed')
  
    for i, facet_name in enumerate(['Accurate passes to final third/90','Accurate progressive passes/90','Fouls per 90']):
        # Add horizontal line
        fig2.add_shape(
        go.layout.Shape(
            type='line',
            x0=0,
            y0=league_avg_values2[facet_name],
            x1=x_max,
            y1=league_avg_values2[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='red', width=1, dash='dash')
              )
          
           )

    # Add vertical line
        fig2.add_shape(
        go.layout.Shape(
            type='line',
            x0=league_avg_values2['Defensive duels per 90'],
            y0=y_min_values[facet_name],
            x1=league_avg_values2['Defensive duels per 90'],
            y1=y_max_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='blue', width=1, dash='dash')
             )
              
              )

    fig2.update_traces(textposition='top center')
    fig2.update_traces(marker=dict(size=8))
    fig2.update_yaxes(matches=None)
    fig2.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    for annotation in fig2.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]

    st.plotly_chart(fig2)

    
    

    df_filtered2['Aerial duels won per 90'] = df_filtered2['Aerial duels per 90'] * (df_filtered2['Aerial duels won, %'] / 100)

    df_filtered2 = df_filtered2.sort_values(by='Aerial duels won per 90', ascending=False)

    fig3 = px.bar(
    df_filtered2, 
    x='Aerial duels won per 90', 
    y='Player', 
    orientation='h', 
    title=f'{position} Aerial wining ability',
    color='Aerial duels won per 90',  # Color based on 'Aerial duels won per 90'
    color_continuous_scale='oranges'  # Color scale from dark to light
    # range_color=[0, max_aerial_duels_won]    
         )

# Reverse the color scale so that higher values are darker
    fig3.update_layout(coloraxis_colorbar=dict(title="Aerial duels won per 90"))
    st.plotly_chart(fig3)
    
# AI model
    #initialize_rag("CB_ElginFC.csv")
    
###################################################### Winger #############################################    
elif position == 'Winger':
    df_position = pvt_df_Wing
    # Dropdown menu for player selection based on position

    original_metrics =[
       'Successful attacking actions per 90',
       'Goals per 90', 'Shots on Target per 90', 'Assists per 90',
       'Accurate Crosses per 90', 'Successful dribbles, %',
       'Offensive duels per 90','Progressive runs per 90', 'Fouls suffered per 90', 'Accurate Passes per 90',
       'Accurate passes to penalty area, %']
    weights=[1,1.1,1,1.25,1,1.2,1,1,0.75,0.9,1.2]    
    weighted_metrics = pd.DataFrame()
    df_position['Shots on Target per 90'] = df_position['Shots per 90'] * (df_position['Shots on target, %'] / 100)
    #df_position['Offensive duels won per 90'] = df_position['Offensive duels per 90'] * (df_position['Offensive duels won, %'] / 100)
    #df_position['Pressing Ability per 90']= df_position['Offensive duels won per 90'] + df_position['Progressive runs per 90']
    df_position['Accurate Passes per 90'] = df_position['Passes per 90'] * (df_position['Accurate passes, %'] / 100)
    df_position['Accurate Crosses per 90'] = df_position['Crosses per 90'] * (df_position['Accurate crosses, %'] / 100)
    
    
    df_position = standardize_and_score_football_metrics(df_position, original_metrics, weights)

    # Dropdown menu for player selection based on position
    if st.sidebar.button('Show Top 5 Players'):
        top_5_players = df_position.nsmallest(5, 'Rank').index.tolist()
    # Multiselect only includes top 5 players
        players_Wing = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
    else:
    # Multiselect includes all players
        players_Wing = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])

    # players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_Wing]
   

    df_filtered2=df_filtered.reset_index()
    
    df_filtered_new=df_position.reset_index()
    
    league_avg_row = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']

# Extract league average values
    league_avg_values = {
    'Successful attacking actions per 90': league_avg_row['Successful attacking actions per 90'].values[0],
    'Shots on Target per 90': league_avg_row['Shots on Target per 90'].values[0],
    'Accurate Crosses per 90': league_avg_row['Accurate Crosses per 90'].values[0],
    # 'Successful dribbles, %': league_avg_row['Successful dribbles, %'].values[0],
    'Accurate passes to penalty area, %': league_avg_row['Accurate passes to penalty area, %'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Successful attacking actions per 90'].max()
    y_max_values = {
    'Shots on Target per 90': df_filtered_new['Shots on Target per 90'].max(),
    'Accurate Crosses per 90': df_filtered_new['Accurate Crosses per 90'].max(),
    # 'Successful dribbles, %': df_filtered_new['Successful dribbles, %'].max(),
    'Accurate passes to penalty area, %': df_filtered_new['Accurate passes to penalty area, %'].max()
           }
    
    
    df_filtered2 = df_filtered2.rename(columns={
                                                'Successful attacking actions per 90': 'Successful Attck. Action/90',
                                                'Accurate passes to penalty area, %': 'Accurate Passes to PA(%)'})
   
    fig = px.scatter(df_filtered2, x='Successful Attck. Action/90', y=['Shots on Target per 90','Accurate Crosses per 90', 'Accurate Passes to PA(%)'], facet_col='variable',
                 facet_col_spacing=0.08, color='Player', title='Pressing Threats vs Final Action')

    for i, facet_name in enumerate(['Shots on Target per 90','Accurate Crosses per 90','Accurate passes to penalty area, %']):
        # Add horizontal line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=0,
            y0=league_avg_values[facet_name],
            x1=x_max,
            y1=league_avg_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='red', width=1, dash='dash')
              )
          
           )

    # Add vertical line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=league_avg_values['Successful attacking actions per 90'],
            y0=0,
            x1=league_avg_values['Successful attacking actions per 90'],
            y1=y_max_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='blue', width=1, dash='dash')
             )
              
              )

    fig.update_traces(textposition='top center')
    fig.update_traces(marker=dict(size=8))
    fig.update_yaxes(matches=None)
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    
    for annotation in fig.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig)
    
   
    # Create radar chart for selected players
    df_position2=df_filtered.drop(columns=[ 'Position', 'Age', 'Matches played','Team',
       'Minutes played', 'Score','Score(0-100)', 'Rank','Goals',
        'Assists','Shots per 90', 'Shots on target, %', 
       'Crosses per 90', 'Accurate crosses, %', 
        'Passes per 90',
       'Accurate passes, %' ])
                              
    radar_fig =create_radar_chart(df_position2, players_Wing, id_column='Player', title=f'Radar Chart for Selected {position} (Default: League Average)')
    st.plotly_chart(radar_fig)

    # Create Gauge chart for selected players
    st.write("Player Ratings Gauge Chart")
    df_filtered_guage=df_filtered.reset_index()
    league_average_rating = df_filtered_new.loc[df_filtered_new['Player'] == 'League Two Average', 'Score(0-100)'].values[0]
    players = df_filtered_guage['Player'].tolist()
    ratings = df_filtered_guage['Score(0-100)'].tolist()
    ranks = df_filtered_guage['Rank'].tolist()
    Age = df_filtered_guage['Age'].tolist()
    Team = df_filtered_guage['Team'].tolist()
    Matches=df_filtered_guage['Matches played'].tolist()
    Minutes=df_filtered_guage['Minutes played'].tolist()
    Position=df_filtered_guage['Position'].tolist()

    for i in range(0, len(players), 3):  # 3 charts per row
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(players):
                with cols[j]:
                    fig = create_gauge_chart(players[i + j], ratings[i + j], ranks[i + j],Age[i + j], Team[i + j], Matches[i + j], Minutes[i + j],Position[i + j],league_average_rating)
                    st.plotly_chart(fig)


    
    league_avg_values2 = {
    'Fouls suffered per 90': league_avg_row['Fouls suffered per 90'].values[0],
    'Offensive duels per 90': league_avg_row['Offensive duels per 90'].values[0],
    'Progressive runs per 90': league_avg_row['Progressive runs per 90'].values[0],
          }
    x_min, x_max = df_filtered_new['Fouls suffered per 90'].min(), df_filtered_new['Fouls suffered per 90'].max()
    y_min, y_max = df_filtered_new['Offensive duels per 90'].min(), df_filtered_new['Offensive duels per 90'].max()
    y_min_drib, y_max_drib = df_filtered_new['Progressive runs per 90'].min(), df_filtered_new['Progressive runs per 90'].max()
    # Create the subplots
    fig_drib = make_subplots(
    rows=1, cols=2, shared_xaxes=True,
    subplot_titles=['Progressive runs vs Foul suffered','Offensive duels vs Foul suffered'],
    specs=[[{"secondary_y": True}, {"secondary_y": True}]]
     )

# Define color sequence for players
    color_sequence = px.colors.qualitative.Plotly

# First subplot for Pressing Ability per 90
    for i, player in enumerate(df_filtered2['Player'].unique()):
        player_data = df_filtered2[df_filtered2['Player'] == player]
        fig_drib.add_trace(
            go.Scatter(
            x=player_data['Fouls suffered per 90'],
            y=player_data['Progressive runs per 90'],
            mode='markers',
            marker=dict(color=color_sequence[i % len(color_sequence)]),
            name=player,
            text=player,
            showlegend=False,    
            textposition='top center'
                 ),
            row=1, col=1, secondary_y=False
               )
        fig_drib.add_shape(
            go.layout.Shape(
        type='line',
        x0=x_min,
        y0=league_avg_values2['Progressive runs per 90'], 
        x1=x_max,
        y1=league_avg_values2['Progressive runs per 90'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             )
             )

        fig_drib.add_shape(
            go.layout.Shape(
        type='line',
        x0=league_avg_values2['Fouls suffered per 90'], 
        y0=y_min_drib,
        x1=league_avg_values2['Fouls suffered per 90'],
        y1=y_max_drib,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              )
           )
            

# Second subplot for Successful dribbles, %
    for i, player in enumerate(df_filtered2['Player'].unique()):
        player_data = df_filtered2[df_filtered2['Player'] == player]
        fig_drib.add_trace(
           go.Scatter(
               x=player_data['Fouls suffered per 90'],
               y=player_data['Offensive duels per 90'],
               mode='markers',
               marker=dict(color=color_sequence[i % len(color_sequence)]),
               name=player,
               text=player,
               showlegend=True,
               textposition='top center'
                  ),   
               row=1, col=2, secondary_y=False
                   )
        fig_drib.add_shape(
            go.layout.Shape(
        type='line',
        x0=x_min,
        y0=league_avg_values2['Offensive duels per 90'], 
        x1=x_max,
        y1=league_avg_values2['Offensive duels per 90'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             ),
            row=1, col=2
             )

        fig_drib.add_shape(
            go.layout.Shape(
        type='line',
        x0=league_avg_values2['Fouls suffered per 90'], 
        y0=y_min,
        x1=league_avg_values2['Fouls suffered per 90'],
        y1=y_max,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              ),
            row=1, col=2
           )
         
           
    
    
    fig_drib.update_xaxes(title_text="Fouls suffered per 90")

    fig_drib.update_yaxes(title_text="Progressive runs per 90", row=1, col=1)
    fig_drib.update_yaxes(title_text="Offensive duels per 90", row=1, col=2)
    fig_drib.update_traces(marker=dict(size=8))

# Display the plot in Streamlit
    st.plotly_chart(fig_drib)
    

    

    df_filtered2['Overall Threats'] = df_filtered2['Goals per 90'] + df_filtered2['Assists per 90'] + df_filtered2['Shots on Target per 90']

# Sorting the DataFrame by 'Goals + Assists per 90', 'Goals per 90', and 'Assists per 90' in descending order
    df_filtered3 = df_filtered2.sort_values(by=['Overall Threats'], ascending=False)


    # df_filtered2 = df_filtered2.sort_values(by=('Aerial duels won, %', ascending=False)

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered3.melt(id_vars='Player', value_vars=['Shots on Target per 90', 'Assists per 90','Goals per 90'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Value', y='Player', color='Metric', orientation='h', title=f'{position} Overall Threats on Goal')
    st.plotly_chart(fig3)

    # Invoke AI
    #initialize_rag("Wing_ElginFC.csv")
    
 ###################################################### Central Forward #############################################     
elif position == 'CF':
    df_position = pvt_df_CF
    # Dropdown menu for player selection based on position

    original_metrics =[
       'Offensive duels won per 90',
        'Goals per 90', 'xG per 90',
        'Accurate passes, %',
       'Accurate Pass to Penalty area','Goal threat per 90',
       'Assists per 90','xA per 90','Goal conversion, %']
    weights=[0.8,1.5,1,0.8,1,1,1.5,1,1.5]
    #weighted_metrics = pd.DataFrame()
    
    df_position['Offensive duels won per 90'] = df_position['Offensive duels per 90'] * (df_position['Offensive duels won, %'] / 100)
    df_position['Shots on Target per 90'] = df_position['Shots per 90'] * (df_position['Shots on target, %'] / 100)
    df_position['Assists per 90']= ((df_position['Assists'] / df_position['Minutes played']) * 90).round(2)
    df_position['Goals per 90']= ((df_position['Goals'] / df_position['Minutes played']) * 90).round(2)
    df_position['Accurate Pass to Penalty area']= df_position['Passes to penalty area per 90'] * (df_position['Accurate passes to penalty area, %']) / 100
    df_position['Goal threat per 90'] = 2 * ((df_position['Touches in box per 90'] + 1) * (df_position['Shots on Target per 90'] + 1)) / ((df_position['Touches in box per 90'] + 1) + (df_position['Shots on Target per 90'] + 1))

    
    df_position = standardize_and_score_football_metrics(df_position, original_metrics, weights)

    if st.sidebar.button('Show Top 5 Players'):
        df_position_reset = df_position.reset_index()
        df_position_sorted = df_position_reset.sort_values(by='Score(0-100)', ascending=False)  # Assuming higher score is better

# Remove duplicates, keeping the one with the highest 'Defender Score(0-100)'
        df_position_unique = df_position_sorted.drop_duplicates(subset='Player', keep='first')

# Step 2: Get the top 5 players
        top_5_df = df_position_unique.head(5) 
        # Extract top 5 player names and their unique identifiers
        top_5_players = top_5_df[['Player', 'Score(0-100)']].set_index('Player').to_dict()['Score(0-100)']
        top_5_player_names = list(top_5_players.keys())
    
    # Multiselect only includes top 5 players
        players_CF = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
        df_filtered2 = df_position_reset[df_position_reset['Player'].isin(players_CF)]
    
    # To ensure only the best rank is retained for each player
        df_filtered2 = df_filtered2.sort_values(by='Score(0-100)', ascending=False)
        df_filtered2 = df_filtered2.drop_duplicates(subset='Player', keep='first')

    else:
    # Multiselect includes all players
        players_CF = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
        df_filtered = df_position.loc[players_CF]
        df_filtered2=df_filtered.reset_index()
    
    df_filtered_new=df_position.reset_index()
   
    league_avg_row = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']

    league_avg_values = {
    'Shots on Target per 90': league_avg_row['Shots on Target per 90'].values[0],
    'Goal conversion, %': league_avg_row['Goal conversion, %'].values[0],
    'xG per 90': league_avg_row['xG per 90'].values[0],
    'Goals per 90': league_avg_row['Goals per 90'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Shots on Target per 90'].max()
    y_max_values = {
    'Goal conversion, %': df_filtered_new['Goal conversion, %'].max(),
    'xG per 90': df_filtered_new['xG per 90'].max(),
    'Goals per 90': df_filtered_new['Goals per 90'].max()
           }
    

   
    fig = px.scatter(df_filtered2, x='Shots on Target per 90', y=['xG per 90','Goals per 90','Goal conversion, %'], facet_col='variable',
                 facet_col_spacing=0.08,color='Player', title='CF Attacking Skills')

    for i, facet_name in enumerate(['xG per 90','Goals per 90','Goal conversion, %']):
        # Add horizontal line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=0,
            y0=league_avg_values[facet_name],
            x1=x_max,
            y1=league_avg_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='red', width=1, dash='dash')
              )
          
           )

    # Add vertical line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=league_avg_values['Shots on Target per 90'],
            y0=0,
            x1=league_avg_values['Shots on Target per 90'],
            y1=y_max_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='blue', width=1, dash='dash')
             )
              
              )

    fig.update_traces(textposition='top center')
    fig.update_traces(marker=dict(size=8))
    fig.update_yaxes(matches=None)
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))

    for annotation in fig.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig)
    

    # Create radar chart for selected players
    df_position2=df_filtered2.drop(columns=[ 'Team','Position',
                        'Matches played', 'Minutes played','Age',
                       'Score(0-100)', 'Rank', 'Score','Goals', 'Passes to penalty area per 90', 'Accurate passes to penalty area, %',
       'Shots per 90','Shots on target, %','xG','xA','Assists',
       'Offensive duels per 90', 'Offensive duels won, %','Shots'
       
                                          ])
                              
    radar_fig =create_radar_chart(df_position2.set_index('Player'), players_CF, id_column='Player', title=f'Radar Chart for Selected {position} (Default: League Average)')
    st.plotly_chart(radar_fig)
    
    # Create Gauge chart for selected players
    st.write("Player Ratings Gauge Chart")
    df_filtered_guage=df_filtered2
    league_average_rating = df_filtered_new.loc[df_filtered_new['Player'] == 'League Two Average', 'Score(0-100)'].values[0]
    players = df_filtered_guage['Player'].tolist()
    ratings = df_filtered_guage['Score(0-100)'].tolist()
    ranks = df_filtered_guage['Rank'].tolist()
    Age = df_filtered_guage['Age'].tolist()
    Team = df_filtered_guage['Team'].tolist()
    Matches=df_filtered_guage['Matches played'].tolist()
    Minutes=df_filtered_guage['Minutes played'].tolist()
    Position=df_filtered_guage['Position'].tolist()

    for i in range(0, len(players), 3):  # 3 charts per row
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(players):
                with cols[j]:
                    fig = create_gauge_chart(players[i + j], ratings[i + j], ranks[i + j],Age[i + j], Team[i + j], Matches[i + j], Minutes[i + j],Position[i + j],league_average_rating)
                    st.plotly_chart(fig)



    league_avg_values2 = {
    'Goal threat per 90': league_avg_row['Goal threat per 90'].values[0],
    'Goals per 90': league_avg_row['Goals per 90'].values[0],
    'Assists per 90': league_avg_row['Assists per 90'].values[0],
    'Offensive duels won per 90': league_avg_row['Offensive duels won per 90'].values[0],
      }
# get max value for X and Y to create quadrants
    x_max2 = df_filtered_new['Goal threat per 90'].max()
    y_max_values2 = {
    'Goals per 90': df_filtered_new['Goals per 90'].max(),
    'Assists per 90': df_filtered_new['Assists per 90'].max(),
    'Offensive duels won per 90': df_filtered_new['Offensive duels won per 90'].max()
           }
    
    
    fig2 = px.scatter(df_filtered2, x='Goal threat per 90', y=['Goals per 90','Assists per 90','Offensive duels won per 90'],facet_col='variable',
                  facet_col_spacing=0.08,color='Player',title=f'{position} Goal Threat by Different Action')
  
    for i, facet_name in enumerate(['Goals per 90','Assists per 90','Offensive duels won per 90']):
        # Add horizontal line
        fig2.add_shape(
        go.layout.Shape(
            type='line',
            x0=0,
            y0=league_avg_values2[facet_name],
            x1=x_max2,
            y1=league_avg_values2[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='red', width=1, dash='dash')
              )
          
           )

    # Add vertical line
        fig2.add_shape(
        go.layout.Shape(
            type='line',
            x0=league_avg_values2['Goal threat per 90'],
            y0=0,
            x1=league_avg_values2['Goal threat per 90'],
            y1=y_max_values2[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='blue', width=1, dash='dash')
             )
              
              )

    fig2.update_traces(textposition='top center')
    fig2.update_traces(marker=dict(size=8))
    fig2.update_yaxes(matches=None)
    fig2.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    for annotation in fig2.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig2)

    

    df_filtered2['Overall Threat Expectation'] = df_filtered2['xG per 90'] + df_filtered2['xA per 90']

# Sorting the DataFrame by 'Goals + Assists per 90', 'Goals per 90', and 'Assists per 90' in descending order
    df_filtered3 = df_filtered2.sort_values(by=['Overall Threat Expectation'], ascending=False)

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered3.melt(id_vars='Player', value_vars=['xG per 90','xA per 90'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Value', y='Player', color='Metric', orientation='h', title=f'{position} Attacking Expectation')
    st.plotly_chart(fig3)

    
    # Input field for user prompt
    # user_prompt = st.text_input("Enter your query:")
    #initialize_rag("CF_ElginFC.csv")
    


###################################################### Goal Keeper #############################################     
elif position == 'GK':
    df_position = pvt_df_GK
    # Dropdown menu for player selection based on position

    original_metrics =[
       'Conceded goals per 90','xG against per 90','Prevented goals per 90',
        'Save rate, %', 'Exits per 90', 'Aerial duels per 90']
    weights=[-1.25,-1,1.25,1.1,1,1]
    #weighted_metrics = pd.DataFrame()
    df_position['Saved Goal']= df_position['Shots against'] - df_position['Conceded goals']
    df_position['Saved Goal per 90']= (df_position['Saved Goal'] / df_position['Minutes played']) * 90
    
    df_position = standardize_and_score_football_metrics(df_position, original_metrics, weights)

    if st.sidebar.button('Show Top 5 Players'):
        top_5_players = df_position.nsmallest(5,'Rank').index.tolist()
    # Multiselect only includes top 5 players
        players_GK = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
    else:
    # Multiselect includes all players
        players_GK = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])

    # players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_GK]
    
    df_filtered2=df_filtered.reset_index()
    
    df_filtered_new=df_position.reset_index()
    
    league_avg_row = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']

    league_avg_values = {
    'Shots against per 90': league_avg_row['Shots against per 90'].values[0],
    'xG against per 90': league_avg_row['xG against per 90'].values[0],
    'Conceded goals per 90': league_avg_row['Conceded goals per 90'].values[0],
    'Saved Goal per 90': league_avg_row['Saved Goal per 90'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Shots against per 90'].max()
    y_max_values = {
    'xG against per 90': df_filtered_new['xG against per 90'].max(),
    'Conceded goals per 90': df_filtered_new['Conceded goals per 90'].max(),
    'Saved Goal per 90': df_filtered_new['Saved Goal per 90'].max()
           }
    y_min_values= {
    'xG against per 90': 0,
    'Conceded goals per 90': 0,
    'Saved Goal per 90':0,# df_filtered_new['Saved Goal per 90'].min()
           }
    

   
    fig = px.scatter(df_filtered2, x='Shots against per 90', y=['xG against per 90','Conceded goals per 90','Saved Goal per 90'], facet_col='variable',
                 facet_col_spacing=0.08, color='Player', title='GK Stats against Shots')

    for i, facet_name in enumerate(['xG against per 90','Conceded goals per 90','Saved Goal per 90']):
        # Add horizontal line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=0,
            y0=league_avg_values[facet_name],
            x1=x_max,
            y1=league_avg_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='red', width=1, dash='dash')
              )
          
           )

    # Add vertical line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=league_avg_values['Shots against per 90'],
            y0=y_min_values[facet_name],
            x1=league_avg_values['Shots against per 90'],
            y1=y_max_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='blue', width=1, dash='dash')
             )
              
              )

    fig.update_traces(textposition='top center')
    fig.update_traces(marker=dict(size=8))
    fig.update_yaxes(matches=None)
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    for annotation in fig.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig)
    

    # Create radar chart for selected players
    df_position2=df_filtered.drop(columns=[ 'Team','Position',
                        'Matches played', 'Minutes played','Age',
                       'Score(0-100)', 'Rank', 'Score',
                            'Saved Goal per 90', 'Saved Goal','Conceded goals', 
         'Prevented goals','Shots against' ])
                              
    radar_fig =create_radar_chart(df_position2, players_GK, id_column='Player', title=f'Radar Chart for Selected {position} (Default:League Average)')
    st.plotly_chart(radar_fig)
    # Create Gauge chart for selected players
    st.write("Player Ratings Gauge Chart")
    df_filtered_guage=df_filtered2
    league_average_rating = df_filtered_new.loc[df_filtered_new['Player'] == 'League Two Average', 'Score(0-100)'].values[0]
    players = df_filtered_guage['Player'].tolist()
    ratings = df_filtered_guage['Score(0-100)'].tolist()
    ranks = df_filtered_guage['Rank'].tolist()
    Age = df_filtered_guage['Age'].tolist()
    Team = df_filtered_guage['Team'].tolist()
    Matches=df_filtered_guage['Matches played'].tolist()
    Minutes=df_filtered_guage['Minutes played'].tolist()
    Position=df_filtered_guage['Position'].tolist()

    for i in range(0, len(players), 3):  # 3 charts per row
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(players):
                with cols[j]:
                    fig = create_gauge_chart(players[i + j], ratings[i + j], ranks[i + j],Age[i + j], Team[i + j], Matches[i + j], Minutes[i + j],Position[i + j],league_average_rating)
                    st.plotly_chart(fig)



    
    
    league_avg_values2 = {
    'xG against per 90': league_avg_row['xG against per 90'].values[0],
    'Prevented goals per 90': league_avg_row['Prevented goals per 90'].values[0],
    'Prevented goals per 90': league_avg_row['Prevented goals per 90'].values[0],
    'Save rate, %': league_avg_row['Save rate, %'].values[0]
          }

    # calculate min, max for the quadrants
    y_min, y_max = df_filtered_new['Prevented goals per 90'].min(), df_filtered_new['Prevented goals per 90'].max()
    x_min, x_max = df_filtered_new['xG against per 90'].min(), df_filtered_new['xG against per 90'].max()
    x_min_mp, x_max_mp = df_filtered_new['Prevented goals per 90'].min(), df_filtered_new['Prevented goals per 90'].max()
    y_min_cs, y_max_cs = df_filtered_new['Save rate, %'].min(), df_filtered_new['Save rate, %'].max()

    fig2 = px.scatter(df_filtered.reset_index(), x='xG against per 90', y='Prevented goals per 90',
                     color='Player', title=f'{position} xG vs Prevention')
    
    
  
    fig2.add_shape(
    go.layout.Shape(
        type='line',
        x0=x_min,
        y0=league_avg_values2['Prevented goals per 90'], 
        x1=x_max,
        y1=league_avg_values2['Prevented goals per 90'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             )
             )

    fig2.add_shape(
    go.layout.Shape(
        type='line',
        x0=league_avg_values2['xG against per 90'], 
        y0=y_min,
        x1=league_avg_values2['xG against per 90'],
        y1=y_max,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              )
           )
  
    fig2.update_traces(textposition='top center')
    fig2.update_traces(marker=dict(size=8))
 
    
    fig3 = px.scatter(df_filtered.reset_index(), x='Prevented goals per 90', y='Save rate, %',
                     color='Player', title=f'{position} Save vs Prevention')
    
    
  
    fig3.add_shape(
    go.layout.Shape(
        type='line',
        x0=x_min_mp,
        y0=league_avg_values2['Save rate, %'], 
        x1=x_max_mp,
        y1=league_avg_values2['Save rate, %'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             )
             )

    fig3.add_shape(
    go.layout.Shape(
        type='line',
        x0=league_avg_values2['Prevented goals per 90'], 
        y0=y_min_cs,
        x1=league_avg_values2['Prevented goals per 90'],
        y1=y_max_cs,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              )
           )
    fig3.update_traces(textposition='top center')
    fig3.update_traces(marker=dict(size=8))
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig2)
    with col2:
         st.plotly_chart(fig3)
   

    

    df_filtered2['Action on Goal Lines'] = df_filtered2['Exits per 90'] + df_filtered2['Aerial duels per 90']

# Sorting the DataFrame by 'Goals + Assists per 90', 'Goals per 90', and 'Assists per 90' in descending order
    df_filtered3 = df_filtered2.sort_values(by=['Action on Goal Lines'], ascending=False)

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered3.melt(id_vars='Player', value_vars=['Exits per 90', 'Aerial duels per 90'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Value', y='Player', color='Metric', orientation='h', title=f'{position} Actions on Goal Lines')
    st.plotly_chart(fig3)

    
    # Input field for user prompt
    # user_prompt = st.text_input("Enter your query:")
    #initialize_rag("GK_ElginFC.csv")
    

###################################################### Full Back #############################################  
elif position == 'FB':
    df_position = pvt_df_FB

    original_metrics =[
       'Defensive duels won per 90','Aerial duels won per 90',
       'Interceptions per 90',  'Accurate crosses per 90',
       'Accurate forward passes, %', 'Accurate long passes, %',
       'Accurate passes to final third/90']
    weights=[1.25,1.2,1.2,1,0.8,0.9,0.8]
   # weighted_metrics = pd.DataFrame()
    
    df_position['Aerial duels won per 90'] = df_position['Aerial duels per 90'] * (df_position['Aerial duels won, %'] / 100)
    df_position['Defensive duels won per 90'] = df_position['Defensive duels per 90'] * (df_position['Defensive duels won, %'] / 100)
    df_position['Accurate passes to final third/90'] = df_position['Passes to final third per 90'] * (df_position['Accurate passes to final third, %'] / 100)
    df_position['Accurate crosses per 90'] = df_position['Crosses per 90'] * (df_position['Accurate crosses, %'] / 100)

    df_position = standardize_and_score_football_metrics(df_position, original_metrics, weights)

    if st.sidebar.button('Show Top 5 Players'):
        df_position_reset = df_position.reset_index()
        df_position_sorted = df_position_reset.sort_values(by='Score(0-100)', ascending=False)  # Assuming higher score is better

# Remove duplicates, keeping the one with the highest 'Defender Score(0-100)'
        df_position_unique = df_position_sorted.drop_duplicates(subset='Player', keep='first')

# Step 2: Get the top 5 players
        top_5_df = df_position_unique.head(5) 
        # Extract top 5 player names and their unique identifiers
        top_5_players = top_5_df[['Player', 'Score(0-100)']].set_index('Player').to_dict()['Score(0-100)']
        top_5_player_names = list(top_5_players.keys())
    
    # Multiselect only includes top 5 players
        players_FB = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
        df_filtered2 = df_position_reset[df_position_reset['Player'].isin(players_FB)]
    
    # To ensure only the best rank is retained for each player
        df_filtered2 = df_filtered2.sort_values(by='Score(0-100)', ascending=False)
        df_filtered2 = df_filtered2.drop_duplicates(subset='Player', keep='first')

    else:
    # Multiselect includes all players
        players_FB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
        df_filtered = df_position.loc[players_FB]
        df_filtered2=df_filtered.reset_index()

    # players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    # df_filtered = df_position.loc[players_FB]
    df_filtered_new=df_position.reset_index()
    league_avg_row = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']

# Extract league average values
    league_avg_values = {
    'Accurate long passes, %': league_avg_row['Accurate long passes, %'].values[0],
    'Defensive duels won per 90': league_avg_row['Defensive duels won per 90'].values[0],
    'Interceptions per 90': league_avg_row['Interceptions per 90'].values[0],
    'Aerial duels won per 90': league_avg_row['Aerial duels won per 90'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Accurate long passes, %'].max()
    y_max_values = {
    'Defensive duels won per 90': df_filtered_new['Defensive duels won per 90'].max(),
    'Interceptions per 90': df_filtered_new['Interceptions per 90'].max(),
    'Aerial duels won per 90': df_filtered_new['Aerial duels won per 90'].max()
           }
    y_min_values = {
    'Defensive duels won per 90': df_filtered_new['Defensive duels won per 90'].min(),
    'Interceptions per 90': df_filtered_new['Interceptions per 90'].min(),
    'Aerial duels won per 90': df_filtered_new['Aerial duels won per 90'].min()
           }
    # y_max = max(y_max_values.values())

    # df_filtered2=df_filtered.reset_index()

    #df_filtered2 = df_filtered2.rename(columns={'Successful defensive actions per 90': 'Successful def. Action/90'})
   
    # df_filtered2 = df_filtered2.rename(columns={'Successful defensive actions per 90': 'Successful def. Action/90'})

   
    fig = px.scatter(df_filtered2, x='Accurate long passes, %', y=['Defensive duels won per 90', 'Interceptions per 90', 'Aerial duels won per 90'], facet_col='variable',
                facet_col_spacing=0.08,  color='Player',  title='Defensive Action vs Passing skills')

    for i, facet_name in enumerate(['Defensive duels won per 90', 'Interceptions per 90', 'Aerial duels won per 90']):
        # Add horizontal line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=0,
            y0=league_avg_values[facet_name],
            x1=x_max,
            y1=league_avg_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='red', width=1, dash='dash')
              )
          
           )

    # Add vertical line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=league_avg_values['Accurate long passes, %'],
            y0=y_min_values[facet_name],
            x1=league_avg_values['Accurate long passes, %'],
            y1=y_max_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='blue', width=1, dash='dash')
             )
              
              )

    fig.update_traces(textposition='top center')
    fig.update_traces(marker=dict(size=8))
    fig.update_yaxes(matches=None)
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    for annotation in fig.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig)
  

    # Create radar chart for selected players
    df_position2=df_filtered2.drop(columns=[ 'Score','Score(0-100)','Rank','Team','Position','Age',
                        'Matches played','Minutes played',
                        'Accurate crosses per 90', 'Accurate passes to final third/90',
                        'Defensive duels per 90','Defensive duels won, %', 'Aerial duels per 90', 'Aerial duels won, %',
        'Crosses per 90','Passes to final third per 90'])
                              
    radar_fig =create_radar_chart(df_position2.set_index('Player'), players_FB, id_column='Player', title=f'Radar Chart for Selected {position} (Default: League Average)')
    st.plotly_chart(radar_fig)
    
    # Create Gauge chart for selected players
    st.write("Player Ratings Gauge Chart")
    df_filtered_guage=df_filtered2
    league_average_rating = df_filtered_new.loc[df_filtered_new['Player'] == 'League Two Average', 'Score(0-100)'].values[0]
    players = df_filtered_guage['Player'].tolist()
    ratings = df_filtered_guage['Score(0-100)'].tolist()
    ranks = df_filtered_guage['Rank'].tolist()
    Age = df_filtered_guage['Age'].tolist()
    Team = df_filtered_guage['Team'].tolist()
    Matches=df_filtered_guage['Matches played'].tolist()
    Minutes=df_filtered_guage['Minutes played'].tolist()
    Position=df_filtered_guage['Position'].tolist()

    for i in range(0, len(players), 3):  # 3 charts per row
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(players):
                with cols[j]:
                    fig = create_gauge_chart(players[i + j], ratings[i + j], ranks[i + j],Age[i + j], Team[i + j], Matches[i + j], Minutes[i + j],Position[i + j],league_average_rating)
                    st.plotly_chart(fig)

    league_avg_values = {
    'Accurate forward passes, %': league_avg_row['Accurate forward passes, %'].values[0],
    'Accurate long passes, %': league_avg_row['Accurate long passes, %'].values[0],
    'Accurate passes to final third, %': league_avg_row['Accurate passes to final third, %'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Accurate forward passes, %'].max()
    y_max_values = {
    'Accurate long passes, %': df_filtered_new['Accurate long passes, %'].max(),
    'Accurate passes to final third, %': df_filtered_new['Accurate passes to final third, %'].max()
           }
    y_min_values = {
    'Accurate long passes, %': df_filtered_new['Accurate long passes, %'].min(),
    'Accurate passes to final third, %': df_filtered_new['Accurate passes to final third, %'].min()
           }
    
    fig2 = px.scatter(df_filtered2, x='Accurate forward passes, %', y=['Accurate long passes, %', 'Accurate passes to final third, %'], facet_col='variable',
                 facet_col_spacing=0.08, color='Player',  title='FB Passing Skills')

    for i, facet_name in enumerate(['Accurate long passes, %', 'Accurate passes to final third, %']):
        # Add horizontal line
        fig2.add_shape(
        go.layout.Shape(
            type='line',
            x0=0,
            y0=league_avg_values[facet_name],
            x1=x_max,
            y1=league_avg_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='red', width=1, dash='dash')
              )
          
           )

    # Add vertical line
        fig2.add_shape(
        go.layout.Shape(
            type='line',
            x0=league_avg_values['Accurate forward passes, %'],
            y0=y_min_values[facet_name],
            x1=league_avg_values['Accurate forward passes, %'],
            y1=y_max_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='blue', width=1, dash='dash')
             )
              
              )

    fig2.update_traces(textposition='top center')
    fig2.update_traces(marker=dict(size=8))
    fig2.update_yaxes(matches=None)
    fig2.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    for annotation in fig2.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]

    st.plotly_chart(fig2)
    

    # df_filtered2['Aerial duels won per 90'] = df_filtered2['Aerial duels per 90'] * (df_filtered2['Aerial duels won, %'] / 100)

    df_filtered2 = df_filtered2.sort_values(by='Accurate crosses per 90', ascending=False)

    fig3 = px.bar(
    df_filtered2, 
    x='Accurate crosses per 90', 
    y='Player', 
    orientation='h', 
    title=f'{position} Crossing Skills',
    color='Accurate crosses per 90',  # Color based on 'Aerial duels won per 90'
    color_continuous_scale='oranges'  # Color scale from dark to light
    # range_color=[0, max_aerial_duels_won]    
         )

# Reverse the color scale so that higher values are darker
    fig3.update_layout(coloraxis_colorbar=dict(title="Accurate crosses per 90"))
    st.plotly_chart(fig3)
    
# AI model
    #initialize_rag("FB_ElginFC.csv")
    

###################################################### Center Attacking Midfielder #############################################  
elif position == 'CAM':
    df_position = pvt_df_CAM

    original_metrics =[
        'Assists per 90','Successful defensive actions per 90', 'Successful attacking actions per 90',
       'Shots on target, %', 'Successful dribbles, %',
       'Offensive duels won, %', 'Progressive runs per 90',
       'Interceptions per 90', 'Overall Passing Skills per 90','Touches in box per 90','Fouls per 90','Aerial duels won, %']
    weights=[1.2,0.8,1,1,1,1,1,0.8,1.2,1,-1,0.9]
    #weighted_metrics = pd.DataFrame()
    
    df_position['Assists per 90'] = ((df_position['Assists'] / df_position['Minutes played']) * 90).round(2)
    df_position['Accurate passes per 90'] = df_position['Passes per 90'] * (df_position['Accurate passes, %'] / 100)
    df_position['Accurate Forward passes per 90'] = df_position['Forward passes per 90'] * (df_position['Accurate forward passes, %'] / 100)
    df_position['Overall Passing Skills per 90'] = (df_position['Accurate Forward passes per 90'] * 0.2 + 
                                                df_position['Accurate passes per 90'] * 0.2
                                                + df_position['Passes to penalty area per 90'] * 0.3
                                                + df_position['Key passes per 90'] * 0.3)
    
    df_position = standardize_and_score_football_metrics(df_position, original_metrics, weights)

    if st.sidebar.button('Show Top 5 Players'):
        df_position_reset = df_position.reset_index()
        df_position_sorted = df_position_reset.sort_values(by='Score(0-100)', ascending=False)  # Assuming higher score is better

# Remove duplicates, keeping the one with the highest 'Defender Score(0-100)'
        df_position_unique = df_position_sorted.drop_duplicates(subset='Player', keep='first')

# Step 2: Get the top 5 players
        top_5_df = df_position_unique.head(5) 
        # Extract top 5 player names and their unique identifiers
        top_5_players = top_5_df[['Player', 'Score(0-100)']].set_index('Player').to_dict()['Score(0-100)']
        top_5_player_names = list(top_5_players.keys())
    
    # Multiselect only includes top 5 players
        players_CAM = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
        df_filtered2 = df_position_reset[df_position_reset['Player'].isin(players_CAM)]
    
    # To ensure only the best rank is retained for each player
        df_filtered2 = df_filtered2.sort_values(by='Score(0-100)', ascending=False)
        df_filtered2 = df_filtered2.drop_duplicates(subset='Player', keep='first')

    else:
    # Multiselect includes all players
        players_CAM = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
        df_filtered = df_position.loc[players_CAM]
        df_filtered2=df_filtered.reset_index()
    
    df_filtered_new=df_position.reset_index()
   
    league_avg_row = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']

    league_avg_values = {
    'Accurate passes per 90': league_avg_row['Accurate passes per 90'].values[0],
    'Accurate Forward passes per 90': league_avg_row['Accurate Forward passes per 90'].values[0],
    'Passes to penalty area per 90': league_avg_row['Passes to penalty area per 90'].values[0],
    'Key passes per 90': league_avg_row['Key passes per 90'].values[0]
      }
# get max value for X and Y to create quadrants
    x_min, x_max = df_filtered_new['Accurate passes per 90'].min(),df_filtered_new['Accurate passes per 90'].max()
    y_max_values = {
    'Accurate Forward passes per 90': df_filtered_new['Accurate Forward passes per 90'].max(),
    'Passes to penalty area per 90': df_filtered_new['Passes to penalty area per 90'].max(),
    'Key passes per 90': df_filtered_new['Key passes per 90'].max()
           }
    y_min_values= {
    'Accurate Forward passes per 90': df_filtered_new['Accurate Forward passes per 90'].min(),
    'Passes to penalty area per 90': df_filtered_new['Passes to penalty area per 90'].min(),
    'Key passes per 90': df_filtered_new['Key passes per 90'].min()
           }
    
    df_filtered2 = df_filtered2.rename(columns={
                                                'Key passes per 90': 'Key Passes',
                                                'Passes to penalty area per 90': 'penalty area',
                                                'Accurate Forward passes per 90': 'Forward'})
                                      

   
    fig = px.scatter(df_filtered2, x='Accurate passes per 90', y=['Key Passes','penalty area','Forward'], facet_col='variable',
                 facet_col_spacing=0.08,color='Player', title='CAM Passing Skills per 90')

    for i, facet_name in enumerate(['Key passes per 90','Passes to penalty area per 90','Accurate Forward passes per 90']):
        # Add horizontal line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=x_min,
            y0=league_avg_values[facet_name],
            x1=x_max,
            y1=league_avg_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='red', width=1, dash='dash')
              )
          
           )

    # Add vertical line
        fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=league_avg_values['Accurate passes per 90'],
            y0=y_min_values[facet_name],
            x1=league_avg_values['Accurate passes per 90'],
            y1=y_max_values[facet_name],
            xref=f'x{i+1}',
            yref=f'y{i+1}',
            line=dict(color='blue', width=1, dash='dash')
             )
              
              )

    fig.update_traces(textposition='top center')
    fig.update_traces(marker=dict(size=8))
    fig.update_yaxes(matches=None)
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))

    for annotation in fig.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig)
    

    # Create radar chart for selected players
    df_position2=df_filtered2.drop(columns=[ 'Team','Position','Matches played','Minutes played','Age',
                       'Score(0-100)', 'Rank', 'Score', 'Dribbles per 90','Shots per 90','Offensive duels per 90',
        'Accurate passes, %','Passes per 90','Accurate passes per 90','Accurate forward passes, %','Forward passes per 90','Key Passes','penalty area','Forward','Assists'
        ,'Aerial duels per 90'
                                          ])
                              
    radar_fig =create_radar_chart(df_position2.set_index('Player'), players_CAM, id_column='Player', title=f'Radar Chart for Selected {position} (Default: League Average)')
    st.plotly_chart(radar_fig)
    
    # Create Gauge chart for selected players
    st.write("Player Ratings Gauge Chart")
    df_filtered_guage=df_filtered2
    league_average_rating = df_filtered_new.loc[df_filtered_new['Player'] == 'League Two Average', 'Score(0-100)'].values[0]
    players = df_filtered_guage['Player'].tolist()
    ratings = df_filtered_guage['Score(0-100)'].tolist()
    ranks = df_filtered_guage['Rank'].tolist()
    Age = df_filtered_guage['Age'].tolist()
    Team = df_filtered_guage['Team'].tolist()
    Matches=df_filtered_guage['Matches played'].tolist()
    Minutes=df_filtered_guage['Minutes played'].tolist()
    Position=df_filtered_guage['Position'].tolist()

    for i in range(0, len(players), 3):  # 3 charts per row
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(players):
                with cols[j]:
                    fig = create_gauge_chart(players[i + j], ratings[i + j], ranks[i + j],Age[i + j], Team[i + j], Matches[i + j], Minutes[i + j],Position[i + j],league_average_rating)
                    st.plotly_chart(fig)



   
    league_avg_values2 = {
    'Offensive duels won, %': league_avg_row['Offensive duels won, %'].values[0],
    'Offensive duels per 90': league_avg_row['Offensive duels per 90'].values[0],
    'xA per 90': league_avg_row['xA per 90'].values[0],
    'Assists per 90': league_avg_row['Assists per 90'].values[0]
        
          }

    # calculate min, max for the quadrants
    x_min, x_max = df_filtered_new['Offensive duels per 90'].min(), df_filtered_new['Offensive duels per 90'].max()
    y_min, y_max = df_filtered_new['Offensive duels won, %'].min(), df_filtered_new['Offensive duels won, %'].max()
    y_min_pro, y_max_pro = df_filtered_new['xA per 90'].min(), df_filtered_new['xA per 90'].max()
    x_min_pas, x_max_pas = df_filtered_new['Assists per 90'].min(), df_filtered_new['Assists per 90'].max()

    # creating scatter plot
    fig2 = px.scatter(df_filtered2, x='Offensive duels per 90',y='Offensive duels won, %',
                     color='Player', title=f'{position} Offensive skills')
    # Adding quadrants
    fig2.add_shape(
    go.layout.Shape(
        type='line',
        x0=x_min,
        y0=league_avg_values2['Offensive duels won, %'], 
        x1=x_max,
        y1=league_avg_values2['Offensive duels won, %'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             )
             )

    fig2.add_shape(
    go.layout.Shape(
        type='line',
        x0=league_avg_values2['Offensive duels per 90'], 
        y0=y_min,
        x1=league_avg_values2['Offensive duels per 90'],
        y1=y_max,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              )
           )
  
    fig2.update_traces(textposition='top center')
    fig2.update_traces(marker=dict(size=8))
#Create scatter plot
    fig22 = px.scatter(df_filtered2, x='Assists per 90',y='xA per 90',
                     color='Player', title=f'{position} Assist Power')
    # Add quadrants
    fig22.add_shape(
    go.layout.Shape(
        type='line',
        x0=x_min_pas,
        y0=league_avg_values2['xA per 90'], 
        x1=x_max_pas,
        y1=league_avg_values2['xA per 90'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             )
             )

    fig22.add_shape(
    go.layout.Shape(
        type='line',
        x0=league_avg_values2['Assists per 90'], 
        y0=y_min_pro,
        x1=league_avg_values2['Assists per 90'],
        y1=y_max_pro,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              )
           )
  
    fig22.update_traces(textposition='top center')
    fig22.update_traces(marker=dict(size=8))
    col1, col2 = st.columns([1, 1])
    # display visuals 
    with col1:
        st.plotly_chart(fig2)
    with col2:
        st.plotly_chart(fig22)

    
   # Bar plot
    df_filtered2 = df_filtered2.sort_values(by='Successful attacking actions per 90', ascending=False)

    fig3 = px.bar(
    df_filtered2, 
    x='Successful attacking actions per 90', 
    y='Player', 
    orientation='h', 
    title=f'{position} Attacking Actions',
    color='Successful attacking actions per 90',  # Color based on 'Aerial duels won per 90'
    color_continuous_scale='oranges'  # Color scale from dark to light
    # range_color=[0, max_aerial_duels_won]    
         )

# Reverse the color scale so that higher values are darker
    fig3.update_layout(coloraxis_colorbar=dict(title="Successful attacking actions per 90"))
    st.plotly_chart(fig3)

    # Invoke AI
    #initialize_rag("CAM_ElginFC.csv")
    
