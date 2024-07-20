#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from math import pi
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import getpass
import os
# from dotenv import load_dotenv
from langchain import hub
# from langchain.vectorstores import Chroma
# from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
# from chromadb import Chroma
# from langchain_chroma import Chroma
#from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
#from langchain_openai import OpenAIEmbeddings
#from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain_mistralai import ChatMistralAI
#from unstructured.partition.xlsx import partition_xlsx
import networkx as nx
#import pandas as pd
import json
import bs4
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

import streamlit as st

# ******************* Data Loading **************************************
df = pd.read_excel("CM_Elgin.xlsx")
df_CB = pd.read_csv("CB_ElginFC.csv")
df_Wing = pd.read_csv("Wing_ElginFC.csv")
df_CF=pd.read_csv("CF_ElginFC.csv")

pvt_df_CB = pd.DataFrame(df_CB).set_index('Player')
pvt_df_Wing = pd.DataFrame(df_Wing).set_index('Player')
pvt_df_CF = pd.DataFrame(df_CF).set_index('Player')

# Pivot the dataframe
pivot_df = df.pivot(index='Player', columns='Attribute', values='Value')


# def create_radar_chart(df, players, id_column, title=None, max_values=None, padding=1.25):
#     df_selected = df.loc[players]
#     categories = df_selected.columns.tolist()
#     data = df_selected.to_dict(orient='list')
#     ids = df_selected.index.tolist()
    
#     # Check and handle zero division or NaNs in max_values
#     if max_values is None:
#         max_values = {key: padding * max(value) for key, value in data.items()}
#     else:
#         for key, max_val in max_values.items():
#             if max_val == 0 or np.isnan(max_val):
#                 max_values[key] = padding * max(data[key])
                
#     # Normalize the data
#     normalized_data = {}
#     for key, value in data.items():
#         if max_values[key] != 0:  # Avoid division by zero
#             normalized_data[key] = np.array(value) / max_values[key]
#         else:
#             normalized_data[key] = np.zeros(len(value))  # Handle zero division case
    
#     num_vars = len(data.keys())
#     ticks = list(data.keys())
#     ticks += ticks[:1]
#     angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist() + [0]
    
#     # Plotting radar chart
#     fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
#     fig.patch.set_facecolor('black')  # Set figure background to black
#     ax.set_facecolor('grey') 
#     for i, model_name in enumerate(ids):
#         values = [normalized_data[key][i] for key in data.keys()]
#         actual_values = [data[key][i] for key in data.keys()]
#         values += values[:1]  # Close the plot for a better look
#         ax.plot(angles, values, label=model_name)
#         ax.fill(angles, values, alpha=0.15)
#         for angle, value, actual_value in zip(angles, values, actual_values):
#             ax.text(angle, value, f'{actual_value:.1f}', ha='center', va='bottom', fontsize=10, color='black')
            
#     ax.fill(angles, np.ones(num_vars + 1), alpha=0.05)
    
#     ax.set_yticklabels([])
#     ax.set_xticks(angles)
#     ax.set_xticklabels(ticks, color='white',fontsize=10)
#     ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), facecolor='black', edgecolor='white', labelcolor='white')

#     if title is not None:
#         plt.suptitle(title,color='white',fontsize=14)
    
#     return fig

# Custom CSS to adjust the sidebar size
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

# def create_radar_chart(df, players, id_column, title=None, padding=1.25):
#     df_selected = df.loc[players]
#     categories = df_selected.columns.tolist()
    
#     # Convert all data to numeric, coercing errors and filling NaNs with zeros
#     df_selected = df_selected.apply(pd.to_numeric, errors='coerce').fillna(0)
    
#     data = df_selected.to_dict(orient='list')
#     ids = df_selected.index.tolist()

#     max_values = {}
#     for key, value in data.items():
#         if any(pd.isna(value)):
#             data[key] = [0 if pd.isna(v) else v for v in value]
#         max_values[key] = padding * max(value) if max(value) != 0 else 1  # Avoid zero division

#     # Normalize the data
#     normalized_data = {}
#     for key, value in data.items():
#         normalized_data[key] = np.array(value) / max_values[key]

#     num_vars = len(data.keys())
#     ticks = list(data.keys())
#     ticks += ticks[:1]
#     angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist() + [0]

#     # Plotting radar chart
#     fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
#     fig.patch.set_facecolor('black')  # Set figure background to black
#     ax.set_facecolor('grey') 
#     for i, model_name in enumerate(ids):
#         values = [normalized_data[key][i] for key in data.keys()]
#         actual_values = [data[key][i] for key in data.keys()]
#         values += values[:1]  # Close the plot for a better look
#         ax.plot(angles, values, label=model_name)
#         ax.fill(angles, values, alpha=0.15)
#         for angle, value, actual_value in zip(angles, values, actual_values):
#             ax.text(angle, value, f'{actual_value:.1f}', ha='center', va='bottom', fontsize=10, color='black')

#     ax.fill(angles, np.ones(num_vars + 1), alpha=0.05)

#     ax.set_yticklabels([])
#     ax.set_xticks(angles)
#     ax.set_xticklabels(ticks, color='white', fontsize=10)
#     ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), facecolor='white', edgecolor='black', labelcolor='black')

#     if title is not None:
#         plt.suptitle(title, color='white', fontsize=14)

#     return fig

def create_radar_chart(df, players, id_column, title=None, padding=1.25):
    # Ensure the players list is indexing correctly
    df_selected = df.loc[players]
    categories = df_selected.columns.tolist()
    N = len(categories)
    
    # Convert all data to numeric, coercing errors and filling NaNs with zeros
    df_selected = df_selected.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    data = df_selected.to_dict(orient='list')
    ids = df_selected.index.tolist()

    max_values = {}
    for key, value in data.items():
        if any(pd.isna(value)):
            data[key] = [0 if pd.isna(v) else v for v in value]
        max_values[key] = padding * max(value) if max(value) != 0 else 1  # Avoid zero division

    # Normalize the data
    normalized_data = {}
    for key, value in data.items():
        normalized_data[key] = np.array(value) / max_values[key]

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Complete the circle

    # Plotting radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('black')  # Set figure background to black
    ax.set_facecolor('grey')
    for i, model_name in enumerate(ids):
        values = [normalized_data[key][i] for key in data.keys()]
        actual_values = [data[key][i] for key in data.keys()]
        values += values[:1]  # Close the plot for a better look
        ax.plot(angles, values, label=model_name)
        ax.fill(angles, values, alpha=0.15)
        for angle, value, actual_value in zip(angles, values, actual_values):
            ax.text(angle, value, f'{actual_value:.1f}', ha='center', va='bottom', fontsize=10, color='black')

    ax.fill(angles, np.ones(N + 1), alpha=0.05)

    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)
    
    ticks = list(data.keys())
    ticks += ticks[:1]  # Add the first category to the end to close the circle
    ax.set_xticks(angles)
    ax.set_xticklabels(ticks, color='white', fontsize=10)

    for label, angle_rad in zip(ax.get_xticklabels(), angles):
        if angle_rad <= pi/2:
            ha = 'left'
            va = "bottom"
            angle_text = angle_rad * (-180 / pi) + 90
        elif pi/2 < angle_rad <= pi:
            ha = 'left'
            va = "top"
            angle_text = angle_rad * (-180 / pi) + 90
        elif pi < angle_rad <= (3 * pi / 2):
            ha = 'right'
            va = "top"
            angle_text = angle_rad * (-180 / pi) - 90
        else:
            ha = 'right'
            va = "bottom"
            angle_text = angle_rad * (-180 / pi) - 90
        label.set_rotation(angle_text)
        label.set_verticalalignment(va)
        label.set_horizontalalignment(ha)
        label.set_color('white') 

    # Draw y-labels
    # ax.set_rlabel_position(0)
    ax.legend(loc='lower right', bbox_to_anchor=(0.1, 0.1), facecolor='white', edgecolor='black', labelcolor='black')

    if title is not None:
        plt.suptitle(title, color='white', fontsize=14)

    return fig
# def create_radar_chart(df, players, id_column, title=None, max_values=None, padding=1.25):
#     df_selected = df.loc[players]
#     categories = df_selected.columns.tolist()
#     data = df_selected.to_dict(orient='list')
#     ids = df_selected.index.tolist()
    
#     if max_values is None:
#         max_values = {key: padding * max(value) for key, value in data.items()}
#     else:
#         for key, max_val in max_values.items():
#             if max_val == 0 or np.isnan(max_val):
#                 max_values[key] = padding * max(data[key])
                
#     normalized_data = {}
#     for key, value in data.items():
#         if max_values[key] != 0:
#             normalized_data[key] = np.array(value) / max_values[key]
#         else:
#             normalized_data[key] = np.zeros(len(value))
    
#     fig = go.Figure()

#     for i, model_name in enumerate(ids):
#         values = [normalized_data[key][i] for key in data.keys()]
#         actual_values = [data[key][i] for key in data.keys()]
#         values += values[:1]
#         fig.add_trace(go.Scatterpolar(
#             r=values,
#             theta=categories + [categories[0]],
#             fill='toself',
#             name=model_name
#         ))

#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 visible=True,
#                 range=[0, 1]
#             )),
#         showlegend=True,
#         title=title
#        )
    
#     return fig

# def create_pizza_plot(df, players, categories, title, padding=1.25):
#     N = len(categories)
#     angles = np.linspace(0, 2 * pi, N, endpoint=False).tolist()
#     angles_mids = np.linspace(0, 2 * pi, N, endpoint=False) + (angles[1] / 2)  # Complete the loop

#     fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))
#     # ax = plt.subplot(111, polar=True)
#     fig.patch.set_facecolor('black')  # Set figure background to black
#     ax.set_facecolor('grey') 
#     ax.set_theta_offset(pi / 2)
#     ax.set_theta_direction(-1)
#     ax.set_xticks(angles_mids)
#     ax.set_xticklabels(categories, color='white', fontsize=14)
#     # ax.xaxis.set_minor_locator(plt.FixedLocator(angles))

#     # Draw ylabels
#     ax.set_rlabel_position(0)
#     ax.set_yticks([20, 40, 60, 80, 100])
#     ax.set_yticklabels(["20", "40", "60", "80", "100"], color="white", size=8)
#     ax.set_ylim(0, 100)
#     width = angles[1] - angles[0]


#     for player in players:
#         values = df.loc[player, categories].values.flatten().tolist()
#         ax.bar(angles_mids, values, width=width, alpha=0.5, edgecolor='k', linewidth=1,label=player)

#     ax.grid(True, axis='x', which='minor')
#     ax.grid(False, axis='x', which='major')
#     ax.grid(True, axis='y', which='major')
#     ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), fontsize=14, facecolor='white', edgecolor='black', labelcolor='black')
#     plt.title(title,color='white', fontsize=14)

#     return fig
# RAG Pipeline for Chatting
mistral_api_key = st.sidebar.text_input('MISTRAL API Key')
api_token = st.sidebar.text_input('API Key', type='password')





# Streamlit app
st.title('Player Performance Dashboard')

default_position_index = ["GK","FB","CB","CM","CAM","Winger","CF"].index('CM')
position = st.sidebar.selectbox('Select position:', options=["GK","FB","CB","CM","CAM","Winger","CF"],index=default_position_index)

# Initialize df_position and default player list
# Initialize df_position and default player list
# df_position = None

# Determine the dataframe to use based on selected position
# if position == 'CM':
#     df_position = pivot_df
# elif position == 'CB':
#     df_position_CB = pvt_df_CB
# # Add other positions here with elif statements

# Ensure df_position is selected
if position == 'CM':
    df_position = pivot_df
    # Dropdown menu for player selection based on position
    players_CM = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_CM]
    # Create point facet graph
    # Create point facet graph
    

    fig = px.scatter(df_filtered.reset_index(), x='Passes per 90', y=[ 'Progressive passes per 90', 'Passes to final third per 90'], facet_col='variable',
                                color='Player',title='Passing threats')

    fig.update_traces(textposition='top center')
    fig.update_traces(marker=dict(size=8))
    for annotation in fig.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig)
    
    #st.plotly_chart(fig)
    # Ensure 'League Two Average' is included in the list of selected players
    # if 'League Two Average' not in players:
    #     players.append('League Two Average')

    # pizza_fig=create_pizza_plot(df_filtered, players_CM, categories=['Accurate forward passes, %', 'Accurate passes to final third, %', 'Accurate passes, %',
    #                     'Accurate progressive passes, %','Aerial duels won, %'], title='Pizza Plot for Selected Players')

    # Create radar chart for selected players
    df_position2=df_filtered.drop(columns=['Accurate forward passes, %', 'Accurate passes to final third, %', 'Accurate passes, %',
                        'Accurate progressive passes, %','Aerial duels won, %','Passes per 90','Progressive passes per 90', 
                              'Passes to final third per 90','Successful defensive actions per 90','Fouls per 90'])
                              
    radar_fig =create_radar_chart(df_position2, players_CM, id_column='Player', title=f'Radar Chart for Selected {position} Players and League Average')
    st.pyplot(radar_fig)
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.pyplot(radar_fig)
    # with col2:
    #     st.pyplot(pizza_fig)

    fig2 = px.scatter(df_filtered.reset_index(), x='Successful defensive actions per 90', y='Fouls per 90',
                     color='Player', title=f'{position} Defensive ability')
  
    fig2.update_traces(textposition='top center')
    fig2.update_traces(marker=dict(size=8))

    df_filtered2 = df_filtered.reset_index()
    

    df_filtered2['Aerial duels won per 90'] = df_filtered2['Aerial duels per 90'] * (df_filtered2['Aerial duels won, %'] / 100)

    df_filtered3 = df_filtered2.sort_values(by='Aerial duels won per 90', ascending=False)

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered3.melt(id_vars='Player', value_vars=['Aerial duels per 90', 'Aerial duels won per 90'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Player', y='Value', color='Metric', title=f'{position} Aerial ability (Stacked)')
    

    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.plotly_chart(fig2)
    with col2:
        st.plotly_chart(fig3)
    # Input field for user prompt
   
    if not mistral_api_key or not api_token:
        st.error("Please provide both the MISTRAL API Key and the API Key.")
    else:
        try:
            # Initialize the LLM model
            llm = ChatMistralAI(model="mistral-large-latest", temperature=0, api_key=mistral_api_key)

        # Loading document through loader
            loader = CSVLoader("CM_ElginFC.csv", encoding="windows-1252")
            docs = loader.load()
        # st.write("Documents loaded successfully.")
  
        # Initialize HuggingFaceHubEmbeddings with the provided API token
            embedding = HuggingFaceHubEmbeddings(huggingfacehub_api_token=api_token)
        # st.write("HuggingFaceHubEmbeddings initialized successfully.")

        # Initialize Chroma vector store
            try:
                vectorstore = FAISS.from_documents(documents=docs, embedding=embedding)
                retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 20, 'fetch_k': 50})
            # st.success("Chroma vector store initialized successfully.")
            except Exception as e:
                 logging.error(f"Error initializing Chroma vector store: {str(e)}")
            # st.error(f"Error initializing Chroma vector store: {str(e)}")
        # Preparing Prompt for Q/A
            system_prompt = (
             "You are an assistant for question-answering tasks. "
             "Use the following pieces of retrieved context to answer "
             "the question. If you don't know the answer, say that you "
             "don't know. Use three sentences maximum and keep the "
             "answer concise."
             "\n\n"
             "{context}"
              )

            prompt = ChatPromptTemplate.from_messages(
                  [
                   ("system", system_prompt),
                    ("human", "{input}"),
                     ]
                    )

            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)
            user_prompt = st.text_input("Enter your query:")
            if user_prompt:
    # Get response from RAG chain
                   response = rag_chain.invoke({"input": user_prompt})
                   st.write(response["answer"])

        # st.success("Chroma vector store initialized successfully.")
        except Exception as e:
                logging.error(f"Error: {str(e)}")
    

######################################################Center Back#############################################    
elif position == 'CB':
    df_position = pvt_df_CB
    # Dropdown menu for player selection based on position
    players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_CB]

   
    fig = px.scatter(df_filtered.reset_index(), x='Fouls per 90', y=['Interceptions per 90', 'PAdj Interceptions', 'PAdj Sliding tackles'], facet_col='variable',
                 color='Player',  title='Defensive Clearance against Foul Committed')

    fig.update_traces(textposition='top center')
    fig.update_traces(marker=dict(size=8))
    for annotation in fig.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig)
    
    #st.plotly_chart(fig)
    # Ensure 'League Two Average' is included in the list of selected players
    # if 'League Two Average' not in players:
    #     players.append('League Two Average')

    pizza_fig=create_pizza_plot(df_filtered, players_CB, categories=['Defensive duels won, %', 'Accurate passes to final third, %',
                        'Accurate progressive passes, %','Aerial duels won, %'], title='Pizza Plot for Selected Players')

    # Create radar chart for selected players
    df_position2=df_filtered.drop(columns=[ 'Accurate passes to final third, %','Team','Contract Expiry \n(Trnsfmkt)','Defensive duels won, %',
                        'Accurate progressive passes, %','Aerial duels won, %','Interceptions per 90','Successful defensive actions per 90','Fouls per 90'])
                              
    radar_fig =create_radar_chart(df_position2, players_CB, id_column='Player', title=f'Radar Chart for Selected {position} Players and League Average')

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(radar_fig)
    with col2:
        st.pyplot(pizza_fig)

    fig2 = px.scatter(df_filtered.reset_index(), x='Defensive duels per 90', y='Defensive duels won, %',
                     color='Player', title=f'{position} Defensive Strength')
  
    fig2.update_traces(textposition='top center')
    fig2.update_traces(marker=dict(size=2))

    df_filtered2=df_filtered.reset_index()
    

    df_filtered2['Aerial duels won per 90'] = df_filtered2['Aerial duels per 90'] * (df_filtered2['Aerial duels won, %'] / 100)

    df_filtered2 = df_filtered2.sort_values(by='Aerial duels won, %', ascending=False)

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered2.melt(id_vars='Player', value_vars=['Aerial duels per 90', 'Aerial duels won per 90'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Player', y='Value', color='Metric', title=f'{position} Aerial ability (Stacked)')
    

    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.plotly_chart(fig2)
    with col2:
        st.plotly_chart(fig3)
    # Input field for user prompt
    # user_prompt = st.text_input("Enter your query:")
    if not mistral_api_key or not api_token:
        st.error("Please provide both the MISTRAL API Key and the API Key.")
    else:
        try:
            # Initialize the LLM model
            llm = ChatMistralAI(model="mistral-large-latest", temperature=0, api_key=mistral_api_key)

        # Loading document through loader
            loader = CSVLoader("CB_ElginFC.csv", encoding="windows-1252")
            docs = loader.load()
        # st.write("Documents loaded successfully.")
  
        # Initialize HuggingFaceHubEmbeddings with the provided API token
            embedding = HuggingFaceHubEmbeddings(huggingfacehub_api_token=api_token)
        # st.write("HuggingFaceHubEmbeddings initialized successfully.")

        # Initialize Chroma vector store
            try:
                vectorstore = FAISS.from_documents(documents=docs, embedding=embedding)
                retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 20, 'fetch_k': 50})
            # st.success("Chroma vector store initialized successfully.")
            except Exception as e:
                 logging.error(f"Error initializing Chroma vector store: {str(e)}")
            # st.error(f"Error initializing Chroma vector store: {str(e)}")
        # Preparing Prompt for Q/A
            system_prompt = (
             "You are an assistant for question-answering tasks. "
             "Use the following pieces of retrieved context to answer "
             "the question. If you don't know the answer, say that you "
             "don't know. Use three sentences maximum and keep the "
             "answer concise."
             "\n\n"
             "{context}"
              )

            prompt = ChatPromptTemplate.from_messages(
                  [
                   ("system", system_prompt),
                    ("human", "{input}"),
                     ]
                    )

            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)
            user_prompt = st.text_input("Enter your query:")
            if user_prompt:
    # Get response from RAG chain
                   response = rag_chain.invoke({"input": user_prompt})
                   st.write(response["answer"])

        # st.success("Chroma vector store initialized successfully.")
        except Exception as e:
                logging.error(f"Error: {str(e)}")
###################################################### Winger #############################################    
elif position == 'Winger':
    df_position = pvt_df_Wing
    # Dropdown menu for player selection based on position
    players_Wing = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_Wing]

    df_filtered2=df_filtered.reset_index()
    df_filtered2['Shots on Target per 90'] = df_filtered2['Shots per 90'] * (df_filtered2['Shots on target, %'] / 100)
    df_filtered2['Offensive duels won per 90'] = df_filtered2['Offensive duels per 90'] * (df_filtered2['Offensive duels won, %'] / 100)
    df_filtered2['Pressing Ability per 90']= df_filtered2['Offensive duels won per 90'] + df_filtered2['Progressive runs per 90']
    

   
    fig = px.scatter(df_filtered2, x='Pressing Ability per 90', y=['Shots on Target per 90','Goals per 90', 'Assists per 90'], facet_col='variable',
                 color='Player', title='Pressing Threats vs Final Action')

    fig.update_traces(textposition='top center')
    fig.update_traces(marker=dict(size=8))
    for annotation in fig.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig)
    
    #st.plotly_chart(fig)
    # Ensure 'League Two Average' is included in the list of selected players
    # if 'League Two Average' not in players:
    #     players.append('League Two Average')

    pizza_fig=create_pizza_plot(df_filtered, players_Wing, categories=['Shots on target, %', 'Accurate crosses, %',
                        'Offensive duels won, %','Successful dribbles, %', 'Accurate passes, %','Accurate passes to penalty area, %'], title='Pizza Plot for Selected Players')

    # Create radar chart for selected players
    df_position2=df_filtered.drop(columns=[ 'Team','Contract Expiry \n(Trnsfmkt)',
                        'Shots on target, %', 'Accurate crosses, %','Assists','Progressive runs per 90',
                        'Offensive duels won, %','Successful dribbles, %', 'Accurate passes, %','Accurate passes to penalty area, %'])
                              
    radar_fig =create_radar_chart(df_position2, players_Wing, id_column='Player', title=f'Radar Chart for Selected {position} Players and League Average')

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(radar_fig)
    with col2:
        st.pyplot(pizza_fig)

    
    # Create the subplots
    fig = make_subplots(
    rows=1, cols=2, shared_xaxes=True,
    subplot_titles=['Pressing Ability per 90', 'Successful dribbles, %'],
    specs=[[{"secondary_y": True}, {"secondary_y": True}]]
     )

# Define color sequence for players
    color_sequence = px.colors.qualitative.Plotly

# First subplot for Pressing Ability per 90
    for i, player in enumerate(df_filtered2['Player'].unique()):
        player_data = df_filtered2[df_filtered2['Player'] == player]
        fig.add_trace(
            go.Scatter(
            x=player_data['Fouls suffered per 90'],
            y=player_data['Pressing Ability per 90'],
            mode='markers',
            marker=dict(color=color_sequence[i % len(color_sequence)]),
            name=player,
            text=player,
            showlegend=False,    
            textposition='top center'
                 ),
            row=1, col=1, secondary_y=False
               )
            

# Second subplot for Successful dribbles, %
    for i, player in enumerate(df_filtered2['Player'].unique()):
        player_data = df_filtered2[df_filtered2['Player'] == player]
        fig.add_trace(
           go.Scatter(
               x=player_data['Fouls suffered per 90'],
               y=player_data['Successful dribbles, %'],
               mode='markers',
               marker=dict(color=color_sequence[i % len(color_sequence)]),
               name=player,
               text=player,
               showlegend=True,
               textposition='top center'
                  ),   
               row=1, col=2, secondary_y=False
                   )
         
           

    fig.update_xaxes(title_text="Fouls suffered per 90")

    fig.update_yaxes(title_text="Pressing Ability per 90", row=1, col=1)
    fig.update_yaxes(title_text="Successful dribbles, %", row=1, col=2)
    fig.update_traces(marker=dict(size=8))

# Display the plot in Streamlit
    st.plotly_chart(fig)
    
    # fig2 = px.scatter(df_filtered2, x='Successful dribbles, %', y=['Pressing Ability per 90','Fouls suffered per 90'],facet_col='variable',
    #                  color='Player',text='Player', title=f'{position} Dribbling vs Pressing skills and Foul suffered')
  
    # fig2.update_traces(textposition='top center')
    # st.plotly_chart(fig2)

    

    df_filtered2['Overall attacking strength'] = df_filtered2['Goals per 90'] + df_filtered2['Assists per 90'] + df_filtered2['Successful attacking actions per 90']

# Sorting the DataFrame by 'Goals + Assists per 90', 'Goals per 90', and 'Assists per 90' in descending order
    df_filtered3 = df_filtered2.sort_values(by=['Overall attacking strength'], ascending=False)


    # df_filtered2 = df_filtered2.sort_values(by=('Aerial duels won, %', ascending=False)

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered3.melt(id_vars='Player', value_vars=['Successful attacking actions per 90', 'Assists per 90','Goals per 90'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Value', y='Player', color='Metric', orientation='h', title=f'{position} Attacking Action')
    st.plotly_chart(fig3)

    # col1, col2 = st.columns([1.5, 1])
    # with col1:
    #     st.plotly_chart(fig2)
    # with col2:
    #     st.plotly_chart(fig3)
    # Input field for user prompt
    # user_prompt = st.text_input("Enter your query:")
    if not mistral_api_key or not api_token:
        st.error("Please provide both the MISTRAL API Key and the API Key.")
    else:
        try:
            # Initialize the LLM model
            llm = ChatMistralAI(model="mistral-large-latest", temperature=0, api_key=mistral_api_key)

        # Loading document through loader
            loader = CSVLoader("Wing_ElginFC.csv", encoding="windows-1252")
            docs = loader.load()
        # st.write("Documents loaded successfully.")
  
        # Initialize HuggingFaceHubEmbeddings with the provided API token
            embedding = HuggingFaceHubEmbeddings(huggingfacehub_api_token=api_token)
        # st.write("HuggingFaceHubEmbeddings initialized successfully.")

        # Initialize Chroma vector store
            try:
                vectorstore = FAISS.from_documents(documents=docs, embedding=embedding)
                retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 20, 'fetch_k': 50})
            # st.success("Chroma vector store initialized successfully.")
            except Exception as e:
                 logging.error(f"Error initializing Chroma vector store: {str(e)}")
            # st.error(f"Error initializing Chroma vector store: {str(e)}")
        # Preparing Prompt for Q/A
            system_prompt = (
             "You are an assistant for question-answering tasks. "
             "Use the following pieces of retrieved context to answer "
             "the question. If you don't know the answer, say that you "
             "don't know. Use three sentences maximum and keep the "
             "answer concise."
             "\n\n"
             "{context}"
              )

            prompt = ChatPromptTemplate.from_messages(
                  [
                   ("system", system_prompt),
                    ("human", "{input}"),
                     ]
                    )

            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)
            user_prompt = st.text_input("Enter your query:")
            if user_prompt:
    # Get response from RAG chain
                   response = rag_chain.invoke({"input": user_prompt})
                   st.write(response["answer"])

        # st.success("Chroma vector store initialized successfully.")
        except Exception as e:
                logging.error(f"Error: {str(e)}")
 ###################################################### Central Forward #############################################     
elif position == 'CF':
    df_position = pvt_df_CF
    # Dropdown menu for player selection based on position
    players_CF = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_CF]

    df_filtered['Recieve long pass, %']= (df_filtered['Received long passes per 90'] / df_filtered['Received passes per 90']) * 100

    df_filtered2=df_filtered.reset_index()
    df_filtered2['Shots on Target per 90'] = df_filtered2['Shots per 90'] * (df_filtered2['Shots on target, %'] / 100)
    df_filtered2['SuccSuccessful dribbles per 90'] = df_filtered2['Dribbles per 90'] * (df_filtered2['Successful dribbles, %'] / 100)
    
    # df_filtered2['Attacking skills']= df_filtered2['SuccSuccessful dribbles per 90'] + df_filtered2['Received passes per 90'] * 100
    

   
    fig = px.scatter(df_filtered2, x='Shots per 90', y=['Shots on Target per 90','xG per 90','Goals per 90'], facet_col='variable',
                 color='Player', title='Threats on Goal')

    fig.update_traces(textposition='top center')
    fig.update_traces(marker=dict(size=8))
    for annotation in fig.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig)
    
    #st.plotly_chart(fig)
    # Ensure 'League Two Average' is included in the list of selected players
    # if 'League Two Average' not in players:
    #     players.append('League Two Average')

    pizza_fig=create_pizza_plot(df_filtered, players_CF, categories=['Shots on target, %', 'Aerial duels won, %',
                        'Recieve long pass, %','Successful dribbles, %'], title='Pizza Plot for Selected Players')

    # Create radar chart for selected players
    df_position2=df_filtered.drop(columns=[ 'Team','Contract Expiry \n(Trnsfmkt)',
                        'Shots on target, %', 'Aerial duels won, %','Shots per 90',
                       'Recieve long pass, %','Successful dribbles, %', 'Received long passes per 90','Received passes per 90'])
                              
    radar_fig =create_radar_chart(df_position2, players_CF, id_column='Player', title=f'Radar Chart for Selected {position} Players and League Average')

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(radar_fig)
    with col2:
        st.pyplot(pizza_fig)

    
    
    
    fig2 = px.scatter(df_filtered2, x='Touches in box per 90', y=['xG per 90','Goals per 90','Fouls suffered per 90'],facet_col='variable',
                  color='Player',title=f'{position} Touches in box vs Goal threat vs Foul suffered')
  
    fig2.update_traces(textposition='top center')
    fig2.update_traces(marker=dict(size=8))
    for annotation in fig2.layout.annotations:
             if 'variable=' in annotation.text:
                        annotation.text = annotation.text.split('=')[1]
    st.plotly_chart(fig2)

    

    df_filtered2['Overall Goal Threat'] = df_filtered2['Goals per 90'] + df_filtered2['xG per 90'] + df_filtered2['Successful attacking actions per 90']

# Sorting the DataFrame by 'Goals + Assists per 90', 'Goals per 90', and 'Assists per 90' in descending order
    df_filtered3 = df_filtered2.sort_values(by=['Overall Goal Threat'], ascending=False)


    # df_filtered2 = df_filtered2.sort_values(by=('Aerial duels won, %', ascending=False)

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered3.melt(id_vars='Player', value_vars=['Successful attacking actions per 90', 'xG per 90','Goals per 90'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Value', y='Player', color='Metric', orientation='h', title=f'{position} Attacking threats')
    st.plotly_chart(fig3)

    # col1, col2 = st.columns([1.5, 1])
    # with col1:
    #     st.plotly_chart(fig2)
    # with col2:
    #     st.plotly_chart(fig3)
    # Input field for user prompt
    # user_prompt = st.text_input("Enter your query:")
    if not mistral_api_key or not api_token:
        st.error("Please provide both the MISTRAL API Key and the API Key.")
    else:
        try:
            # Initialize the LLM model
            llm = ChatMistralAI(model="mistral-large-latest", temperature=0, api_key=mistral_api_key)

        # Loading document through loader
            loader = CSVLoader("CF_ElginFC.csv", encoding="windows-1252")
            docs = loader.load()
        # st.write("Documents loaded successfully.")
  
        # Initialize HuggingFaceHubEmbeddings with the provided API token
            embedding = HuggingFaceHubEmbeddings(huggingfacehub_api_token=api_token)
        # st.write("HuggingFaceHubEmbeddings initialized successfully.")

        # Initialize Chroma vector store
            try:
                vectorstore = FAISS.from_documents(documents=docs, embedding=embedding)
                retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 20, 'fetch_k': 50})
            # st.success("Chroma vector store initialized successfully.")
            except Exception as e:
                 logging.error(f"Error initializing Chroma vector store: {str(e)}")
            # st.error(f"Error initializing Chroma vector store: {str(e)}")
        # Preparing Prompt for Q/A
            system_prompt = (
             "You are an assistant for question-answering tasks. "
             "Use the following pieces of retrieved context to answer "
             "the question. If you don't know the answer, say that you "
             "don't know. Use three sentences maximum and keep the "
             "answer concise."
             "\n\n"
             "{context}"
              )

            prompt = ChatPromptTemplate.from_messages(
                  [
                   ("system", system_prompt),
                    ("human", "{input}"),
                     ]
                    )

            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)
            user_prompt = st.text_input("Enter your query:")
            if user_prompt:
    # Get response from RAG chain
                   response = rag_chain.invoke({"input": user_prompt})
                   st.write(response["answer"])

        # st.success("Chroma vector store initialized successfully.")
        except Exception as e:
                logging.error(f"Error: {str(e)}")

# players = st.selectbox('Select a player:', options=pivot_df.index.tolist())

# # Filter data for selected player
# #selected_data = pivot_df.loc[[player_selected]]
# st.subheader('Radar Chart for Selected Player and League Average')
# # Create radar chart for selected player
# create_radar_chart(pivot_df, [players, 'League Two Average'], id_column='Player', title=f'Radar Chart for {players} and League Average')



