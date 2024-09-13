#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import seaborn as sns
from scipy.stats import norm
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
# from langchain_mistralai import ChatMistralAI
# from langchain_together import ChatTogether
from langchain_ai21 import ChatAI21
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

import streamlit as st

# ******************* Data Loading **************************************
# df = pd.read_excel("CM_Elgin.xlsx")
df_CM = pd.read_csv("CM_ElginFC.csv",encoding='ISO-8859-1')
df_CB = pd.read_csv("CB_ElginFC.csv")
df_Wing = pd.read_csv("Wing_ElginFC.csv",encoding='ISO-8859-1')
df_CF=pd.read_csv("CF_ElginFC.csv",encoding='ISO-8859-1')
df_GK=pd.read_csv("GK_ElginFC.csv",encoding='ISO-8859-1')
df_FB=pd.read_csv("FB_ElginFC.csv",encoding='ISO-8859-1')

pvt_df_CM = pd.DataFrame(df_CM).set_index('Player')
pvt_df_CB = pd.DataFrame(df_CB).set_index('Player')
pvt_df_Wing = pd.DataFrame(df_Wing).set_index('Player')
df_CF[df_CF.columns[3:]] = df_CF[df_CF.columns[3:]].apply(pd.to_numeric, errors='coerce')
pvt_df_CF = pd.DataFrame(df_CF).set_index('Player')
pvt_df_GK = pd.DataFrame(df_GK).set_index('Player')
pvt_df_FB = pd.DataFrame(df_FB).set_index('Player')

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


# Set the background image
# Set the background image
# background_image = """
# <style>
# [data-testid="stAppViewContainer"] > .main {
#     background-image: url("image/Scotinage.jpg");
#     background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
#     background-position: center;  
#     background-repeat: no-repeat;
# }
# </style>
# """

st.markdown(background_image, unsafe_allow_html=True)

# Pivot the dataframe
# pivot_df = df.pivot(index='Player', columns='Attribute', values='Value')


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

# def create_radar_chart(df, players,id_column, title=None, padding=1.15):
#     # Ensure the players list is indexing correctly
#     df_selected = df.loc[players]
#     categories = df_selected.columns.tolist()
#     N = len(categories)
    
#     # Convert all data to numeric, coercing errors and filling NaNs with zeros
#     df_selected = df_selected.apply(pd.to_numeric, errors='coerce').fillna(0)
    
#     data = df_selected.to_dict(orient='list')
#     ids = df_selected.index.tolist()

#     max_values = {}
#     for key, value in data.items():
#         max_values[key] = padding * max(value) if max(value) != 0 else 1  # Avoid zero division

#     # Normalize the data
#     normalized_data = {}
#     for key, value in data.items():
#         normalized_data[key] = np.array(value) / max_values[key]

#     # Create radar chart
#     fig = go.Figure()

#     for i, model_name in enumerate(ids):
#         values = [normalized_data[key][i] for key in data.keys()]
#         actual_values = [data[key][i] for key in data.keys()]
#         values += values[:1]  # Close the plot for a better look
#         actual_values += actual_values[:1]
#         angles = [n / float(N) * 2 * np.pi for n in range(N)]
#         angles += angles[:1]  # Complete the circle

#         fig.add_trace(go.Scatterpolar(
#             r=values,
#             theta=[categories[j] for j in range(len(categories))] + [categories[0]],
#             mode='lines+markers',
#             name=model_name,
#             hovertemplate='<b>%{theta}</b>: %{r:.1f}<extra></extra>'
#         ))

#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(visible=True),
#             angularaxis=dict(ticks=''),
#         ),
#         showlegend=True,
#         title='Radar Chart'
#     )

#     return fig


# def create_radar_chart(df, players, id_column, title=None, padding=1.15):
#     # Ensure the players list is indexing correctly
#     df_selected = df.loc[players]
#     categories = df_selected.columns.tolist()
#     N = len(categories)
    
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

#     angles = [n / float(N) * 2 * np.pi for n in range(N)]
#     angles += angles[:1]  # Complete the circle

#     # Plotting radar chart
#     fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
#     fig.patch.set_facecolor('black')  # Set figure background to black
#     ax.set_facecolor('white')
#     subplot_df_dict[ax] = df_selected
#     # lines = []
#     for i, model_name in enumerate(ids):
#         values = [normalized_data[key][i] for key in data.keys()]
#         actual_values = [data[key][i] for key in data.keys()]
#         values += values[:1]  # Close the plot for a better look
#         angles_with_end = angles
#         line, = ax.plot(angles_with_end, values, label=model_name)
#         # ax.plot(angles, values, label=model_name)
#         ax.fill(angles_with_end, values, alpha=0.15)
#         # lines.append((line, model_name, actual_values))
#         # def get_tooltip_text(index):
#         #     player = ids[index]
#         #     values_text = ', '.join([f'{cat}: {val:.1f}' for cat, val in zip(categories, actual_values)])
#         #     return f'{player}\n{values_text}'

#         # # Use show_hover_panel for tooltips
#         # cursor = show_hover_panel(df_selected, get_text_func=get_tooltip_text)
#         # cursor.connect("add", lambda sel: sel.annotation.set_text(get_tooltip_text(sel.index)))
#         # for angle, value, actual_value in zip(angles, values, actual_values):
#         #     ax.text(angle, value, f'{actual_value:.1f}', ha='center', va='bottom', fontsize=10, color='black')

#     ax.fill(angles, np.ones(N + 1), alpha=0.05)

#     ax.set_theta_offset(np.pi/2)
#     ax.set_theta_direction(-1)
    
#     ticks = categories
#     ticks += ticks[:1]  # Add the first category to the end to close the circle
#     ax.set_xticks(angles)
#     ax.set_xticklabels(ticks, color='white', fontsize=10)

#     for label, angle_rad in zip(ax.get_xticklabels(), angles):
#         if angle_rad <= pi/2:
#             ha = 'left'
#             va = "bottom"
#             angle_text = angle_rad * (-180 / pi) + 90
#         elif pi/2 < angle_rad <= pi:
#             ha = 'left'
#             va = "top"
#             angle_text = angle_rad * (-180 / pi) + 90
#         elif pi < angle_rad <= (3 * pi / 2):
#             ha = 'right'
#             va = "top"
#             angle_text = angle_rad * (-180 / pi) - 90
#         else:
#             ha = 'right'
#             va = "bottom"
#             angle_text = angle_rad * (-180 / pi) - 90
#         label.set_rotation(angle_text)
#         label.set_verticalalignment(va)
#         label.set_horizontalalignment(ha)
#         label.set_color('white') 

#     # Add tooltips
#     # def hover_annotation(sel):
#     #     line, player_name, actual_values = lines[sel.index]
#     #     angle_idx = np.argmin(np.abs(np.array(angles) - sel.artist.get_data()[0][sel.index]))
#     #     value = actual_values[angle_idx]
#     #     sel.annotation.set_text(f'{player_name}\n{categories[angle_idx]}: {value:.1f}')
    
#     # cursor = mplcursors.cursor([line for line, _, _ in lines], hover=True)
#     # cursor.connect("add", hover_annotation)

#     # Draw y-labels
#     # ax.set_rlabel_position(0)
#     ax.legend(loc='upper right', bbox_to_anchor=(0.05, 0.05), facecolor='white', edgecolor='black', labelcolor='black')
#     show_hover_panel(show_annotation)

#     if title is not None:
#         plt.suptitle(title, color='white', fontsize=14)

#     # def hover_annotation(sel):
#     #     index = sel.index
#     #     angle_idx = int(index % len(angles))  # Determine the index of the angle
#     #     player_name = lines[index][1]
#     #     actual_value = lines[index][2][angle_idx]
#     #     sel.annotation.set_text(f'{player_name}\n{ticks[angle_idx]}: {actual_value:.1f}')
    
#     # cursor = mplcursors.cursor([line for line, _, _ in lines], hover=True)
#     # cursor.connect("add", hover_annotation)
#     return fig
# @st.cache_data
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

#     # global_min = min(min(value) for value in data.values())
#     # global_max = max(max(value) for value in data.values())

#     # # Ensure the global_max is larger than global_min to avoid division by zero
#     # if global_max == global_min:
#     #     global_max += 1e-9  # Small number to avoid zero division
    
#     # # Normalize the data using global min-max normalization
#     # normalized_data = {}
#     # for key, value in data.items():
#     #     # Apply global min-max normalization
#     #     normalized_data[key] = (np.array(value) - global_min) / (global_max - global_min)
#     fig = go.Figure()

#     # color_map = {player: f'rgba({np.random.randint(256)},{np.random.randint(256)},{np.random.randint(256)})' for player in ids}

#     for i, model_name in enumerate(ids):
#         values = [normalized_data[key][i] for key in data.keys()]
#         values += values[:1]  # Complete the circle

#         hovertext = [f"{categories[j]}: {data[c][i]:.2f}" for j, c in enumerate(categories)]
#         hovertext += [hovertext[0]]  # Complete the circle for hovertext

#         fig.add_trace(go.Scatterpolar(
#             r=values,
#             theta=categories + [categories[0]],
#             fill='toself',
#             name=model_name,
#             hoverinfo='text',
#             hovertext=hovertext
#             # line=dict(
#             #     color=color_map[model_name],
#             #     width=1
#             # ),
#             # showlegend=True
#         ))


#     fig.update_traces(
#         hoverlabel=dict(
#             bgcolor='white',  # Background color of the hover label
#             font=dict(
#                 color='black'  # Text color of the hover label
#             )
#         )
#     )
    
#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 visible=True,
#                 range=[0, 1],
#                 # tickvals=[0, 0.5, 1],
#                 # ticktext=['0', '0.5', '1'],
#                 showticklabels=False,
#                 ticks="",
#                 showline=True,
#                 showgrid=True,
#                 gridcolor='gray',
#                 gridwidth=1,
#             ),
#             angularaxis=dict(
#                 tickvals=list(range(len(categories))),
#                 ticktext=categories + [categories[0]],
#                 rotation=0,
#                 direction="clockwise",
#                 showticklabels=True,
#                 ticks="",
#                 showline=True,
#                 showgrid=True,
#                 gridcolor='gray',
#                 gridwidth=1,
                
#                 tickfont=dict(size=8, color='white'),
#             ),
#         ),
#         title=dict(
#             text=title,
#             font=dict(size=12)
#         ),
#         width=1000,  # Increased width for better clarity
#         height=300,  # Increased height for better clarity
#         margin=dict(l=100, r=125, t=18, b=0),  # Increased bottom margin to accommodate the legend
#         paper_bgcolor='black',  # Background color
#         plot_bgcolor='white',    # Plot area background color
#         legend=dict(
#             orientation="v",  # Horizontal orientation
#             yanchor="top",    # Position the legend above the plot area
#             y=-0.1,           # Vertical position (below the plot area)
#             xanchor="right", # Center the legend horizontally
#             x=0.5,            # Horizontal position (centered)
#             bgcolor='white', # Transparent background
#             bordercolor='white',
#             borderwidth=1,
#             font=dict(size=10, color='black')
#         )
        
#     )

#     return fig
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
        margin=dict(l=100, r=125, t=20, b=20),
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

def create_gauge_chart(player_name, rating, rank, age, team, matches_played, minutes_played,league_average_rating):
    # Format the title text with HTML to include additional information
    title_text = f"""
    <span style="font-size:16px"><b>{player_name}</b></span><br>
    <span style="font-size:12px">Rank: {rank}</span><br>
    <span style="font-size:10px">Team: {team}</span><br>
    <span style="font-size:10px">Age: {age} | Matches: {matches_played} | Minutes: {minutes_played}</span>
    """
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
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
        height=300,  # Adjust height to accommodate more text
        width=300, 
        margin=dict(t=50, b=0, l=0, r=0)  # Top margin to give space for title
    )
    return fig
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
AI21_api_key = st.sidebar.text_input('Together API Key')
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
    df_position = pvt_df_CM

    # Assign weights to the metrics based on their importance
    original_metrics =[
       'Assists',
       'Successful defensive actions per 90', 'Aerial duels per 90',
       'Aerial duels won, %', 'Interceptions per 90', 'Fouls per 90',
       'Shots per 90', 'Recieved Passes P/90', 'Passes per 90',
       'Accurate passes, %', 'Forward passes per 90',
       'Accurate forward passes, %', 'Key passes per 90',
       'Passes to final third per 90', 'Accurate passes to final third, %',
       'Progressive passes per 90', 'Accurate progressive passes, %']
    weights=[0.8,1,0.9,0.9,1,-1.25,0.8,1,0.9,1,0.9,1,1,0.9,1,0.9,1]
    weighted_metrics = pd.DataFrame()
    for metric, weight in zip(original_metrics, weights):
        weighted_metrics[metric] = df_position[metric] * weight
    
    # Calculate z-scores for the weighted metrics
    z_scores = pd.DataFrame()
    for metric in original_metrics:
        mean = weighted_metrics[metric].mean()
        std = weighted_metrics[metric].std()
        z_scores[f'{metric} zscore'] = (weighted_metrics[metric] - mean) / std

# Aggregate the z-scores to get a final z-score
    df_position["CM zscore"] = z_scores.mean(axis=1)

# Calculate final z-score and score
    original_mean = df_position["CM zscore"].mean()
    original_std = df_position["CM zscore"].std()
    df_position["CM zscore"] = (df_position["CM zscore"] - original_mean) / original_std
    df_position["CM Score(0-100)"] = (norm.cdf(df_position["CM zscore"]) * 100).round(2)
    df_position['Player Rank'] = df_position['CM Score(0-100)'].rank(ascending=False)

    # Dropdown menu for player selection based on position
    if st.sidebar.button('Show Top 5 Players'):
        top_5_players = df_position.nsmallest(5, 'Player Rank').index.tolist()
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
    'Progressive passes per 90': league_avg_row['Progressive passes per 90'].values[0],
    'Passes to final third per 90': league_avg_row['Passes to final third per 90'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Passes per 90'].max()
    y_max_values = {
    'Forward passes per 90': df_filtered_new['Forward passes per 90'].max(),
    'Progressive passes per 90': df_filtered_new['Progressive passes per 90'].max(),
    'Passes to final third per 90': df_filtered_new['Passes to final third per 90'].max()
           }
    # y_max = max(y_max_values.values())
   
    # create Scatter plot
    fig = px.scatter(df_filtered.reset_index(), x='Passes per 90', y=[ 'Forward passes per 90','Progressive passes per 90', 'Passes to final third per 90'], facet_col='variable',
                                facet_col_spacing=0.08, color='Player',title='Passing threats')
    
    

# Add horizontal and vertical lines for each facet, this will provide the quadrant inside scatter plot
    
    for i, facet_name in enumerate(['Forward passes per 90', 'Progressive passes per 90', 'Passes to final third per 90']):
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
    df_position2=df_filtered.drop(columns=['CM Score(0-100)', 'Contract Expiry \n(Trnsfmkt)','CM zscore','Player Rank','Age','Team', 'Matches played', 'Minutes played'])

    # Rdar chart
    radar_fig =create_radar_chart(df_position2, players_CM, id_column='Player', title=f'Radar Chart for {position} (Default: League Average)')
    st.plotly_chart(radar_fig)
    # Creating Player info table
#     columns_to_display = ['Player','Team','CM Score(0-100)', 'Player Rank','Age', 'Matches played', 'Minutes played' ]
#     df_filtered_display=df_filtered.reset_index()
#     df_filtered_display = df_filtered_display[columns_to_display].rename(columns={
#       'CM Score(0-100)': 'Rating (0-100)',
#       'Matches played': 'Matches played (2023/24)'
#          })
#     df_filtered_display = df_filtered_display.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

# # Style the DataFrame
#     def style_dataframe(df):
#         return df.style.set_table_styles(
#         [
#             {"selector": "thead th", "props": [("font-weight", "bold"), ("background-color", "#4CAF50"), ("color", "white")]},
#             {"selector": "td", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
#             {"selector": "table", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
#         ]
#           ).hide(axis="index")

#     styled_df = style_dataframe(df_filtered_display)
#     st.write("Players Info:")
#     st.dataframe(styled_df, use_container_width=True)

    st.write("Player Ratings Gauge Chart")
    df_filtered_guage=df_filtered.reset_index()
    league_average_rating = df_filtered_new.loc[df_filtered_new['Player'] == 'League Two Average', 'CM Score(0-100)'].values[0]
    players = df_filtered_guage['Player'].tolist()
    ratings = df_filtered_guage['CM Score(0-100)'].tolist()
    ranks = df_filtered_guage['Player Rank'].tolist()
    Age = df_filtered_guage['Age'].tolist()
    Team = df_filtered_guage['Team'].tolist()
    Matches=df_filtered_guage['Matches played'].tolist()
    Minutes=df_filtered_guage['Minutes played'].tolist()

    for i in range(0, len(players), 3):  # 3 charts per row
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(players):
                with cols[j]:
                    fig = create_gauge_chart(players[i + j], ratings[i + j], ranks[i + j],Age[i + j], Team[i + j], Matches[i + j], Minutes[i + j],league_average_rating)
                    st.plotly_chart(fig)

# Display styled DataFrame in Streamlit

    # col1, col2 = st.columns(2)
    # with col1:
    #     st.plotly_chart(radar_fig)
    # with col2:
    #     st.write("Players Info:")
    #     st.dataframe(styled_df, use_container_width=True)
        
   # Calculating Assit per 90 for slected player and for league average 
    df_filtered2 = df_filtered.reset_index()
    df_filtered2['Assists per 90'] = ((df_filtered2['Assists'] / df_filtered2['Minutes played']) * 90).round(2)
    df_filtered_new['Assists per 90']=((df_filtered_new['Assists'] / df_filtered_new['Minutes played']) * 90).round(2)
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
    
    # Calculate Aerial duel won per 90 

    df_filtered2['Aerial duels won per 90'] = df_filtered2['Aerial duels per 90'] * (df_filtered2['Aerial duels won, %'] / 100)

 # sort the vlaues by Aerial duel per 90 CM involved.
    df_filtered3 = df_filtered2.sort_values(by='Aerial duels per 90', ascending=False)

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered3.melt(id_vars='Player', value_vars=['Aerial duels per 90', 'Aerial duels won per 90'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Value', y='Player', color='Metric',orientation='h', title=f'{position} Aerial ability (Stacked)')
    st.plotly_chart(fig3)
    
    # Input field for user prompt
   
    if not AI21_api_key or not api_token:
        st.error("Please provide both the TOGETHER API Key and the API Key.")
    else:
        try:
            # Initialize the LLM model
            llm = ChatAI21(
                 model="jamba-instruct-preview",
#     base_url="https://api.aimlapi.com/chat/completions",
                 api_key=AI21_api_key,
                 max_tokens=4096,
                 temprature=0.7,
                 top_p=1,
                 stop=[],
                  )

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
                retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 20, 'fetch_k': 20})
            # st.success("Chroma vector store initialized successfully.")
            except Exception as e:
                 logging.error(f"Error initializing FAISS vector store: {str(e)}")
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

    original_metrics =[
       'Successful defensive actions per 90', 'Defensive duels per 90',
       'Defensive duels won, %', 'Aerial duels per 90', 'Aerial duels won, %',
       'PAdj Sliding tackles', 'Shots blocked per 90', 'Interceptions per 90',
       'PAdj Interceptions', 'Fouls per 90', 'Passes to final third per 90',
       'Accurate passes to final third, %', 'Progressive passes per 90',
       'Accurate progressive passes, %']
    weights=[1,1,1,1,1,1,1,1,1,-1.25,0.75,0.9,0.8,0.9]
    weighted_metrics = pd.DataFrame()
    for metric, weight in zip(original_metrics, weights):
        weighted_metrics[metric] = df_position[metric] * weight
    
    # Calculate z-scores for the weighted metrics
    z_scores = pd.DataFrame()
    for metric in original_metrics:
        mean = weighted_metrics[metric].mean()
        std = weighted_metrics[metric].std()
        z_scores[f'{metric} zscore'] = (weighted_metrics[metric] - mean) / std

# Aggregate the z-scores to get a final z-score
    df_position["defensive zscore"] = z_scores.mean(axis=1)

# Calculate final z-score and score
    original_mean = df_position["defensive zscore"].mean()
    original_std = df_position["defensive zscore"].std()
    df_position["defensive zscore"] = (df_position["defensive zscore"] - original_mean) / original_std
    df_position["Defender Score(0-100)"] = (norm.cdf(df_position["defensive zscore"]) * 100).round(2)
    df_position['Player Rank'] = df_position['Defender Score(0-100)'].rank(ascending=False)

    # df_position["defensive zscore"] = np.dot(df_position[original_metrics], weights)
    # original_mean = df_position["defensive zscore"].mean()
    # original_std = df_position["defensive zscore"].std()
    # df_position["defensive zscore"] = (df_position["defensive zscore"] - original_mean) / original_std
    # df_position["Defender Score(0-100)"] = (norm.cdf(df_position["defensive zscore"]) * 100).round(2)
    # df_position['Player Rank'] = df_position['Defender Score(0-100)'].rank(ascending=False)
    # Dropdown menu for player selection based on position
    if st.sidebar.button('Show Top 5 Players'):
        top_5_players = df_position.nsmallest(5, 'Player Rank').index.tolist()
    # Multiselect only includes top 5 players
        players_CB = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
    else:
    # Multiselect includes all players
        players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])

    # players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_CB]

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
    # y_max = max(y_max_values.values())

    df_filtered2=df_filtered.reset_index()

    df_filtered2 = df_filtered2.rename(columns={'Successful defensive actions per 90': 'Successful def. Action/90'})
   
    
    fig = px.scatter(df_filtered2, x='Successful def. Action/90', y=['Shots blocked per 90', 'PAdj Interceptions', 'PAdj Sliding tackles'], facet_col='variable',
                 facet_col_spacing=0.08, color='Player',  title='CM Defensive Actions')

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
    df_position2=df_filtered.drop(columns=[ 'defensive zscore','Defender Score(0-100)','Player Rank','Team','Contract Expiry \n(Trnsfmkt)','Age',
                        'Matches played\n(23/24)','Minutes played'])
                              
    radar_fig =create_radar_chart(df_position2, players_CB, id_column='Player', title=f'Radar Chart for Selected {position} Players and League Average')
    # st.pyplot(radar_fig)
    columns_to_display = ['Player','Team','Age', 'Matches played\n(23/24)', 'Minutes played', 'Defender Score(0-100)', 'Player Rank']
    df_filtered_display=df_filtered.reset_index()
    df_filtered_display = df_filtered_display[columns_to_display].rename(columns={
      'Defender Score(0-100)': 'Rating (0-100)',
      'Matches played\n(23/24)': 'Matches played (2023/24)'
         })
    df_filtered_display = df_filtered_display.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

# Style the DataFrame
    def style_dataframe(df):
        return df.style.set_table_styles(
        [
            {"selector": "thead th", "props": [("font-weight", "bold"), ("background-color", "#4CAF50"), ("color", "white")]},
            {"selector": "td", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
            {"selector": "table", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
        ]
          ).hide(axis="index")

    styled_df = style_dataframe(df_filtered_display)

# Display styled DataFrame in Streamlit
    # st.write("Players Info:")
    # st.dataframe(styled_df, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(radar_fig)
    with col2:
        st.write("Players Info:")
        st.dataframe(styled_df, use_container_width=True)

    # league_avg_row2 = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']
    league_avg_values2 = {
    'Defensive duels per 90': league_avg_row['Defensive duels per 90'].values[0],
    'Defensive duels won, %': league_avg_row['Defensive duels won, %'].values[0]
    # 'Interceptions per 90': league_avg_row2['Interceptions per 90'].values[0],
          }
    x_min, x_max = df_filtered_new['Defensive duels per 90'].min(), df_filtered_new['Defensive duels per 90'].max()
    y_min, y_max = df_filtered_new['Defensive duels won, %'].min(), df_filtered_new['Defensive duels won, %'].max()
    # y_min_int, y_max_int = df_filtered_new['Interceptions per 90'].min(), df_filtered_new['Interceptions per 90'].max()

    fig2 = px.scatter(df_filtered2, x='Defensive duels per 90', y='Defensive duels won, %',
                     color='Player', title=f'{position} Defensive Strength')
  
    fig2.add_shape(
    go.layout.Shape(
        type='line',
        x0=x_min,
        y0=league_avg_values2['Defensive duels won, %'], 
        x1=x_max,
        y1=league_avg_values2['Defensive duels won, %'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             )
             )

    fig2.add_shape(
    go.layout.Shape(
        type='line',
        x0=league_avg_values2['Defensive duels per 90'], 
        y0=y_min,
        x1=league_avg_values2['Defensive duels per 90'],
        y1=y_max,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              )
           )
    
    fig2.update_traces(textposition='top center')
    fig2.update_traces(marker=dict(size=8))

    
    

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
    if not Together_api_key or not api_token:
        st.error("Please provide both the TOGETHER API Key and the API Key.")
    else:
        try:
            # Initialize the LLM model
            llm = ChatAI21(
                 model="jamba-instruct-preview",
#     base_url="https://api.aimlapi.com/chat/completions",
                 api_key=AI21_api_key,
                 max_tokens=4096,
                 temprature=0.7,
                 top_p=1,
                 stop=[],
                  )

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
                retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 20, 'fetch_k': 20})
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

    original_metrics =[
       'Assists', 'Successful attacking actions per 90',
       'Goals per 90', 'Shots per 90', 'Shots on target, %', 'Assists per 90',
       'Crosses per 90', 'Accurate crosses, %', 'Successful dribbles, %',
       'Offensive duels per 90', 'Offensive duels won, %',
       'Progressive runs per 90', 'Fouls suffered per 90', 'Passes per 90',
       'Accurate passes, %', 'Accurate passes to penalty area, %']
    weights=[1,1,0.9,0.9,0.9,1,1,1,1,1,1,1,1,1,1,1]    
    weighted_metrics = pd.DataFrame()
    for metric, weight in zip(original_metrics, weights):
        weighted_metrics[metric] = df_position[metric] * weight
    
    # Calculate z-scores for the weighted metrics
    z_scores = pd.DataFrame()
    for metric in original_metrics:
        mean = weighted_metrics[metric].mean()
        std = weighted_metrics[metric].std()
        z_scores[f'{metric} zscore'] = (weighted_metrics[metric] - mean) / std

# Aggregate the z-scores to get a final z-score
    df_position["wing zscore"] = z_scores.mean(axis=1)

# Calculate final z-score and score
    original_mean = df_position["wing zscore"].mean()
    original_std = df_position["wing zscore"].std()
    df_position["wing zscore"] = (df_position["wing zscore"] - original_mean) / original_std
    df_position["wing Score(0-100)"] = (norm.cdf(df_position["wing zscore"]) * 100).round(2)
    df_position['Player Rank'] = df_position['wing Score(0-100)'].rank(ascending=False)

    # df_position["defensive zscore"] = np.dot(df_position[original_metrics], weights)
    # original_mean = df_position["defensive zscore"].mean()
    # original_std = df_position["defensive zscore"].std()
    # df_position["defensive zscore"] = (df_position["defensive zscore"] - original_mean) / original_std
    # df_position["Defender Score(0-100)"] = (norm.cdf(df_position["defensive zscore"]) * 100).round(2)
    # df_position['Player Rank'] = df_position['Defender Score(0-100)'].rank(ascending=False)
    # Dropdown menu for player selection based on position
    if st.sidebar.button('Show Top 5 Players'):
        top_5_players = df_position.nsmallest(5, 'Player Rank').index.tolist()
    # Multiselect only includes top 5 players
        players_Wing = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
    else:
    # Multiselect includes all players
        players_Wing = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])

    # players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_Wing]
    # players_Wing = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    # df_filtered = df_position.loc[players_Wing]

    df_filtered2=df_filtered.reset_index()
    df_filtered2['Shots on Target per 90'] = df_filtered2['Shots per 90'] * (df_filtered2['Shots on target, %'] / 100)
    df_filtered2['Offensive duels won per 90'] = df_filtered2['Offensive duels per 90'] * (df_filtered2['Offensive duels won, %'] / 100)
    df_filtered2['Pressing Ability per 90']= df_filtered2['Offensive duels won per 90'] + df_filtered2['Progressive runs per 90']

    df_filtered_new=df_position.reset_index()
    df_filtered_new['Shots on Target per 90'] = df_filtered_new['Shots per 90'] * (df_filtered_new['Shots on target, %'] / 100)
    df_filtered_new['Offensive duels won per 90'] = df_filtered_new['Offensive duels per 90'] * (df_filtered_new['Offensive duels won, %'] / 100)
    df_filtered_new['Pressing Ability per 90']= df_filtered_new['Offensive duels won per 90'] + df_filtered_new['Progressive runs per 90']
    league_avg_row = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']

# Extract league average values
    league_avg_values = {
    'Pressing Ability per 90': league_avg_row['Pressing Ability per 90'].values[0],
    'Shots on Target per 90': league_avg_row['Shots on Target per 90'].values[0],
    'Goals per 90': league_avg_row['Goals per 90'].values[0],
    'Assists per 90': league_avg_row['Assists per 90'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Pressing Ability per 90'].max()
    y_max_values = {
    'Shots on Target per 90': df_filtered_new['Shots on Target per 90'].max(),
    'Goals per 90': df_filtered_new['Goals per 90'].max(),
    'Assists per 90': df_filtered_new['Assists per 90'].max()
           }
    

   
    fig = px.scatter(df_filtered2, x='Pressing Ability per 90', y=['Shots on Target per 90','Goals per 90', 'Assists per 90'], facet_col='variable',
                 facet_col_spacing=0.08, color='Player', title='Pressing Threats vs Final Action')

    for i, facet_name in enumerate(['Shots on Target per 90','Goals per 90', 'Assists per 90']):
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
            x0=league_avg_values['Pressing Ability per 90'],
            y0=0,
            x1=league_avg_values['Pressing Ability per 90'],
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
    
    #st.plotly_chart(fig)
    # Ensure 'League Two Average' is included in the list of selected players
    # if 'League Two Average' not in players:
    #     players.append('League Two Average')

   
    # Create radar chart for selected players
    df_position2=df_filtered.drop(columns=[ 'Contract Expiry \n(Trnsfmkt)', 'Age', 'Matches played','Team',
       'Minutes played', 'wing zscore','wing Score(0-100)', 'Player Rank'])
                              
    radar_fig =create_radar_chart(df_position2, players_Wing, id_column='Player', title=f'Radar Chart for Selected {position} Players and League Average')
    
    columns_to_display = ['Player','Team','Age', 'Matches played', 'Minutes played', 'wing Score(0-100)', 'Player Rank']
    df_filtered_display=df_filtered.reset_index()
    df_filtered_display = df_filtered_display[columns_to_display].rename(columns={
      'wing Score(0-100)': 'Rating (0-100)',
      'Matches played': 'Matches played (2023/24)'
         })
    df_filtered_display = df_filtered_display.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

# Style the DataFrame
    def style_dataframe(df):
        return df.style.set_table_styles(
        [
            {"selector": "thead th", "props": [("font-weight", "bold"), ("background-color", "#4CAF50"), ("color", "white")]},
            {"selector": "td", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
            {"selector": "table", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
        ]
          ).hide(axis="index")

    styled_df = style_dataframe(df_filtered_display)

# Display styled DataFrame in Streamlit
    # st.write("Players Info:")
    # st.dataframe(styled_df, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(radar_fig)
    with col2:
        st.write("Players Info:")
        st.dataframe(styled_df, use_container_width=True)
    
    league_avg_values2 = {
    'Fouls suffered per 90': league_avg_row['Fouls suffered per 90'].values[0],
    'Pressing Ability per 90': league_avg_row['Pressing Ability per 90'].values[0],
    'Successful dribbles, %': league_avg_row['Successful dribbles, %'].values[0],
          }
    x_min, x_max = df_filtered_new['Fouls suffered per 90'].min(), df_filtered_new['Fouls suffered per 90'].max()
    y_min, y_max = df_filtered_new['Pressing Ability per 90'].min(), df_filtered_new['Pressing Ability per 90'].max()
    y_min_drib, y_max_drib = df_filtered_new['Successful dribbles, %'].min(), df_filtered_new['Successful dribbles, %'].max()
    # Create the subplots
    fig_drib = make_subplots(
    rows=1, cols=2, shared_xaxes=True,
    subplot_titles=['Pressing Ability vs Foul suffered', 'Successful dribbles, % vs Foul suffered'],
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
        fig_drib.add_shape(
            go.layout.Shape(
        type='line',
        x0=x_min,
        y0=league_avg_values2['Pressing Ability per 90'], 
        x1=x_max,
        y1=league_avg_values2['Pressing Ability per 90'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             )
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
              )
           )
            

# Second subplot for Successful dribbles, %
    for i, player in enumerate(df_filtered2['Player'].unique()):
        player_data = df_filtered2[df_filtered2['Player'] == player]
        fig_drib.add_trace(
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
        fig_drib.add_shape(
            go.layout.Shape(
        type='line',
        x0=x_min,
        y0=league_avg_values2['Successful dribbles, %'], 
        x1=x_max,
        y1=league_avg_values2['Successful dribbles, %'],
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
        y0=y_min_drib,
        x1=league_avg_values2['Fouls suffered per 90'],
        y1=y_max_drib,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              ),
            row=1, col=2
           )
         
           
    
    
    fig_drib.update_xaxes(title_text="Fouls suffered per 90")

    fig_drib.update_yaxes(title_text="Pressing Ability per 90", row=1, col=1)
    fig_drib.update_yaxes(title_text="Successful dribbles, %", row=1, col=2)
    fig_drib.update_traces(marker=dict(size=8))

# Display the plot in Streamlit
    st.plotly_chart(fig_drib)
    

    

    df_filtered2['Overall attacking strength'] = df_filtered2['Goals per 90'] + df_filtered2['Assists per 90'] + df_filtered2['Successful attacking actions per 90']

# Sorting the DataFrame by 'Goals + Assists per 90', 'Goals per 90', and 'Assists per 90' in descending order
    df_filtered3 = df_filtered2.sort_values(by=['Overall attacking strength'], ascending=False)


    # df_filtered2 = df_filtered2.sort_values(by=('Aerial duels won, %', ascending=False)

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered3.melt(id_vars='Player', value_vars=['Successful attacking actions per 90', 'Assists per 90','Goals per 90'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Value', y='Player', color='Metric', orientation='h', title=f'{position} Attacking Action')
    st.plotly_chart(fig3)

    # Input for user query
    if not AI21_api_key or not api_token:
        st.error("Please provide both the TOGETHER API Key and the API Key.")
    else:
        try:
            # Initialize the LLM model
            llm = ChatAI21(
                 model="jamba-instruct-preview",
#     base_url="https://api.aimlapi.com/chat/completions",
                 api_key=AI21_api_key,
                 max_tokens=4096,
                 temprature=0.7,
                 top_p=1,
                 stop=[],
                  )

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
                retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 20, 'fetch_k': 20})
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

    original_metrics =[
       'Goals', 'Aerial duels per 90', 'Aerial duels won, %',
       'Successful attacking actions per 90', 'Goals per 90', 'xG per 90',
       'Shots per 90', 'Shots on target, %', 'Dribbles per 90',
       'Successful dribbles, %', 'Touches in box per 90',
       'Received passes per 90', 'Received long passes per 90',
       'Fouls suffered per 90']
    weights=[1,1,1,1,1,1,1,1,0.8,0.8,1,1,0.9,0.9]
    weighted_metrics = pd.DataFrame()
    for metric, weight in zip(original_metrics, weights):
        weighted_metrics[metric] = df_position[metric] * weight
    
    # Calculate z-scores for the weighted metrics
    z_scores = pd.DataFrame()
    for metric in original_metrics:
        mean = weighted_metrics[metric].mean()
        std = weighted_metrics[metric].std()
        z_scores[f'{metric} zscore'] = (weighted_metrics[metric] - mean) / std

# Aggregate the z-scores to get a final z-score
    df_position["CF zscore"] = z_scores.mean(axis=1)

# Calculate final z-score and score
    original_mean = df_position["CF zscore"].mean()
    original_std = df_position["CF zscore"].std()
    df_position["CF zscore"] = (df_position["CF zscore"] - original_mean) / original_std
    df_position["CF Score(0-100)"] = (norm.cdf(df_position["CF zscore"]) * 100).round(2)
    df_position['Player Rank'] = df_position['CF Score(0-100)'].rank(ascending=False)

    # df_position["defensive zscore"] = np.dot(df_position[original_metrics], weights)
    # original_mean = df_position["defensive zscore"].mean()
    # original_std = df_position["defensive zscore"].std()
    # df_position["defensive zscore"] = (df_position["defensive zscore"] - original_mean) / original_std
    # df_position["Defender Score(0-100)"] = (norm.cdf(df_position["defensive zscore"]) * 100).round(2)
    # df_position['Player Rank'] = df_position['Defender Score(0-100)'].rank(ascending=False)
    # Dropdown menu for player selection based on position
    if st.sidebar.button('Show Top 5 Players'):
        top_5_players = df_position.nsmallest(5, 'Player Rank').index.tolist()
    # Multiselect only includes top 5 players
        players_CF = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
    else:
    # Multiselect includes all players
        players_CF = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])

    # players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_CF]
    
    # players_CF = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    # df_filtered = df_position.loc[players_CF]

    df_filtered['Recieve long pass, %']= (df_filtered['Received long passes per 90'] / df_filtered['Received passes per 90']) * 100

    df_filtered2=df_filtered.reset_index()
    df_filtered2['Shots on Target per 90'] = df_filtered2['Shots per 90'] * (df_filtered2['Shots on target, %'] / 100)
    df_filtered2['SuccSuccessful dribbles per 90'] = df_filtered2['Dribbles per 90'] * (df_filtered2['Successful dribbles, %'] / 100)
    
    # df_filtered2['Attacking skills']= df_filtered2['SuccSuccessful dribbles per 90'] + df_filtered2['Received passes per 90'] * 100
    df_filtered_new=df_position.reset_index()
    df_filtered_new['Shots on Target per 90'] = df_filtered_new['Shots per 90'] * (df_filtered_new['Shots on target, %'] / 100)
    df_filtered_new['SuccSuccessful dribbles per 90'] = df_filtered_new['Dribbles per 90'] * (df_filtered_new['Successful dribbles, %'] / 100)
    
    league_avg_row = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']

    league_avg_values = {
    'Shots per 90': league_avg_row['Shots per 90'].values[0],
    'Shots on Target per 90': league_avg_row['Shots on Target per 90'].values[0],
    'xG per 90': league_avg_row['xG per 90'].values[0],
    'Goals per 90': league_avg_row['Goals per 90'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Shots per 90'].max()
    y_max_values = {
    'Shots on Target per 90': df_filtered_new['Shots on Target per 90'].max(),
    'xG per 90': df_filtered_new['xG per 90'].max(),
    'Goals per 90': df_filtered_new['Goals per 90'].max()
           }
    

   
    fig = px.scatter(df_filtered2, x='Shots per 90', y=['Shots on Target per 90','xG per 90','Goals per 90'], facet_col='variable',
                 facet_col_spacing=0.08,color='Player', title='Threats on Goal')

    for i, facet_name in enumerate(['Shots on Target per 90','xG per 90','Goals per 90']):
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
            x0=league_avg_values['Shots per 90'],
            y0=0,
            x1=league_avg_values['Shots per 90'],
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
    df_position2=df_filtered.drop(columns=[ 'Team','Contract Expiry \n(Trnsfmkt)',
                        'Matches played', 'Minutes played','Age',
                       'CF Score(0-100)', 'Player Rank', 'CF zscore'])
                              
    radar_fig =create_radar_chart(df_position2, players_CF, id_column='Player', title=f'Radar Chart for Selected {position} Players and League Average')
    
    columns_to_display = ['Player','Team','Age', 'Matches played', 'Minutes played', 'CF Score(0-100)', 'Player Rank']
    df_filtered_display=df_filtered.reset_index()
    df_filtered_display = df_filtered_display[columns_to_display].rename(columns={
      'CF Score(0-100)': 'Rating (0-100)',
      'Matches played': 'Matches played (2023/24)'
         })
    df_filtered_display = df_filtered_display.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

# Style the DataFrame
    def style_dataframe(df):
        return df.style.set_table_styles(
        [
            {"selector": "thead th", "props": [("font-weight", "bold"), ("background-color", "#4CAF50"), ("color", "white")]},
            {"selector": "td", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
            {"selector": "table", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
        ]
          ).hide(axis="index")

    styled_df = style_dataframe(df_filtered_display)

# Display styled DataFrame in Streamlit
    # st.write("Players Info:")
    # st.dataframe(styled_df, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(radar_fig)
    with col2:
        st.write("Players Info:")
        st.dataframe(styled_df, use_container_width=True)
    

    league_avg_values2 = {
    'Touches in box per 90': league_avg_row['Touches in box per 90'].values[0],
    'xG per 90': league_avg_row['xG per 90'].values[0],
    'Goals per 90': league_avg_row['Goals per 90'].values[0],
    'Fouls suffered per 90': league_avg_row['Fouls suffered per 90'].values[0],
      }
# get max value for X and Y to create quadrants
    x_max2 = df_filtered_new['Touches in box per 90'].max()
    y_max_values2 = {
    'xG per 90': df_filtered_new['xG per 90'].max(),
    'Goals per 90': df_filtered_new['Goals per 90'].max(),
    'Fouls suffered per 90': df_filtered_new['Fouls suffered per 90'].max()
           }
    
    
    fig2 = px.scatter(df_filtered2, x='Touches in box per 90', y=['xG per 90','Goals per 90','Fouls suffered per 90'],facet_col='variable',
                  facet_col_spacing=0.08,color='Player',title=f'{position} Touches in box vs Goal threat vs Foul suffered')
  
    for i, facet_name in enumerate(['xG per 90','Goals per 90','Fouls suffered per 90']):
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
            x0=league_avg_values2['Touches in box per 90'],
            y0=0,
            x1=league_avg_values2['Touches in box per 90'],
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

    

    df_filtered2['Overall Goal Threat'] = df_filtered2['Goals per 90'] + df_filtered2['xG per 90'] + df_filtered2['Successful attacking actions per 90']

# Sorting the DataFrame by 'Goals + Assists per 90', 'Goals per 90', and 'Assists per 90' in descending order
    df_filtered3 = df_filtered2.sort_values(by=['Overall Goal Threat'], ascending=False)

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered3.melt(id_vars='Player', value_vars=['Successful attacking actions per 90', 'xG per 90','Goals per 90'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Value', y='Player', color='Metric', orientation='h', title=f'{position} Attacking threats')
    st.plotly_chart(fig3)

    
    # Input field for user prompt
    # user_prompt = st.text_input("Enter your query:")
    if not AI21_api_key or not api_token:
        st.error("Please provide both the TOGETHER API Key and the API Key.")
    else:
        try:
            # Initialize the LLM model
            llm = ChatAI21(
                 model="jamba-instruct-preview",
#     base_url="https://api.aimlapi.com/chat/completions",
                 api_key=AI21_api_key,
                 max_tokens=4096,
                 temprature=0.7,
                 top_p=1,
                 stop=[],
                  )

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
                retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 103, 'fetch_k': 103})
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


###################################################### Goal Keeper #############################################     
elif position == 'GK':
    df_position = pvt_df_GK
    # Dropdown menu for player selection based on position

    original_metrics =[
       'Conceded goals', 'Conceded goals per 90',
       'xG against', 'xG against per 90', 'Prevented goals',
       'Prevented goals per 90',
       'Clean sheets', 'Save rate, %', 'Exits per 90', 'Aerial duels per 90']
    weights=[-1,-1.25,-0.9,-0.9,1,1,1.25,1,1,1]
    weighted_metrics = pd.DataFrame()
    for metric, weight in zip(original_metrics, weights):
        weighted_metrics[metric] = df_position[metric] * weight
    
    # Calculate z-scores for the weighted metrics
    z_scores = pd.DataFrame()
    for metric in original_metrics:
        mean = weighted_metrics[metric].mean()
        std = weighted_metrics[metric].std()
        z_scores[f'{metric} zscore'] = (weighted_metrics[metric] - mean) / std

# Aggregate the z-scores to get a final z-score
    df_position["GK zscore"] = z_scores.mean(axis=1)

# Calculate final z-score and score
    original_mean = df_position["GK zscore"].mean()
    original_std = df_position["GK zscore"].std()
    df_position["GK zscore"] = (df_position["GK zscore"] - original_mean) / original_std
    df_position["GK Score(0-100)"] = (norm.cdf(df_position["GK zscore"]) * 100).round(2)
    df_position['Player Rank'] = df_position['GK Score(0-100)'].rank(ascending=False)

    # df_position["defensive zscore"] = np.dot(df_position[original_metrics], weights)
    # original_mean = df_position["defensive zscore"].mean()
    # original_std = df_position["defensive zscore"].std()
    # df_position["defensive zscore"] = (df_position["defensive zscore"] - original_mean) / original_std
    # df_position["Defender Score(0-100)"] = (norm.cdf(df_position["defensive zscore"]) * 100).round(2)
    # df_position['Player Rank'] = df_position['Defender Score(0-100)'].rank(ascending=False)
    # Dropdown menu for player selection based on position
    if st.sidebar.button('Show Top 5 Players'):
        top_5_players = df_position.nsmallest(5, 'Player Rank').index.tolist()
    # Multiselect only includes top 5 players
        players_GK = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
    else:
    # Multiselect includes all players
        players_GK = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['L1 & L2 Average'])

    # players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_GK]
    
    # players_CF = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    # df_filtered = df_position.loc[players_CF]

    # df_filtered['Recieve long pass, %']= (df_filtered['Received long passes per 90'] / df_filtered['Received passes per 90']) * 100

    df_filtered2=df_filtered.reset_index()
    # df_filtered2['Shots on Target per 90'] = df_filtered2['Shots per 90'] * (df_filtered2['Shots on target, %'] / 100)
    # df_filtered2['SuccSuccessful dribbles per 90'] = df_filtered2['Dribbles per 90'] * (df_filtered2['Successful dribbles, %'] / 100)
    
    # df_filtered2['Attacking skills']= df_filtered2['SuccSuccessful dribbles per 90'] + df_filtered2['Received passes per 90'] * 100
     # df_filtered2['Attacking skills']= df_filtered2['SuccSuccessful dribbles per 90'] + df_filtered2['Received passes per 90'] * 100
    df_filtered_new=df_position.reset_index()
    
    league_avg_row = df_filtered_new[df_filtered_new['Player'] == 'L1 & L2 Average']

    league_avg_values = {
    'Shots against per 90': league_avg_row['Shots against per 90'].values[0],
    'xG against per 90': league_avg_row['xG against per 90'].values[0],
    'Conceded goals per 90': league_avg_row['Conceded goals per 90'].values[0],
    'Prevented goals per 90': league_avg_row['Prevented goals per 90'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Shots against per 90'].max()
    y_max_values = {
    'xG against per 90': df_filtered_new['xG against per 90'].max(),
    'Conceded goals per 90': df_filtered_new['Conceded goals per 90'].max(),
    'Prevented goals per 90': df_filtered_new['Prevented goals per 90'].max()
           }
    y_min_values= {
    'xG against per 90': 0,
    'Conceded goals per 90': 0,
    'Prevented goals per 90': df_filtered_new['Prevented goals per 90'].min()
           }
    

   
    fig = px.scatter(df_filtered2, x='Shots against per 90', y=['xG against per 90','Conceded goals per 90','Prevented goals per 90'], facet_col='variable',
                 facet_col_spacing=0.08, color='Player', title='GK Stats against Shots')

    for i, facet_name in enumerate(['xG against per 90','Conceded goals per 90','Prevented goals per 90']):
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
    df_position2=df_filtered.drop(columns=[ 'Team','Contract Expiry \n(Trnsfmkt)',
                        'Matches played', 'Minutes played','Age',
                       'GK Score(0-100)', 'Player Rank', 'GK zscore'])
                              
    radar_fig =create_radar_chart(df_position2, players_GK, id_column='Player', title=f'Radar Chart for Selected {position} Players and League Average')
    
    columns_to_display = ['Player','Team','Age', 'Matches played', 'Minutes played', 'GK Score(0-100)', 'Player Rank']
    df_filtered_display=df_filtered.reset_index()
    df_filtered_display = df_filtered_display[columns_to_display].rename(columns={
      'GK Score(0-100)': 'Rating (0-100)',
      'Matches played': 'Matches played (2023/24)'
         })
    df_filtered_display = df_filtered_display.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

# Style the DataFrame
    def style_dataframe(df):
        return df.style.set_table_styles(
        [
            {"selector": "thead th", "props": [("font-weight", "bold"), ("background-color", "#4CAF50"), ("color", "white")]},
            {"selector": "td", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
            {"selector": "table", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
        ]
          ).hide(axis="index")

    styled_df = style_dataframe(df_filtered_display)

# Display styled DataFrame in Streamlit
    # st.write("Players Info:")
    # st.dataframe(styled_df, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(radar_fig)
    with col2:
        st.write("Players Info:")
        st.dataframe(styled_df, use_container_width=True)
    

    
    
    league_avg_values2 = {
    'Shots against': league_avg_row['Shots against'].values[0],
    'Save rate, %': league_avg_row['Save rate, %'].values[0],
    'Matches played': league_avg_row['Matches played'].values[0],
    'Clean sheets': league_avg_row['Clean sheets'].values[0]
          }

    # calculate min, max for the quadrants
    x_min, x_max = df_filtered_new['Shots against'].min(), df_filtered_new['Shots against'].max()
    y_min, y_max = df_filtered_new['Save rate, %'].min(), df_filtered_new['Save rate, %'].max()
    x_min_mp, x_max_mp = df_filtered_new['Matches played'].min(), df_filtered_new['Matches played'].max()
    y_min_cs, y_max_cs = df_filtered_new['Clean sheets'].min(), df_filtered_new['Clean sheets'].max()

    fig2 = px.scatter(df_filtered.reset_index(), x='Shots against', y='Save rate, %',
                     color='Player', title=f'{position} Saving Strength')
    
    
  
    fig2.add_shape(
    go.layout.Shape(
        type='line',
        x0=x_min,
        y0=league_avg_values2['Save rate, %'], 
        x1=x_max,
        y1=league_avg_values2['Save rate, %'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             )
             )

    fig2.add_shape(
    go.layout.Shape(
        type='line',
        x0=league_avg_values2['Shots against'], 
        y0=y_min,
        x1=league_avg_values2['Shots against'],
        y1=y_max,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              )
           )
  
    fig2.update_traces(textposition='top center')
    fig2.update_traces(marker=dict(size=8))
    # for annotation in fig2.layout.annotations:
    #          if 'variable=' in annotation.text:
    #                     annotation.text = annotation.text.split('=')[1]
    
    
    fig3 = px.scatter(df_filtered.reset_index(), x='Matches played', y='Clean sheets',
                     color='Player', title=f'{position} Clean sheets vs Matches Played')
    
    
  
    fig3.add_shape(
    go.layout.Shape(
        type='line',
        x0=x_min_mp,
        y0=league_avg_values2['Clean sheets'], 
        x1=x_max_mp,
        y1=league_avg_values2['Clean sheets'],
        line=dict(color='red', width=1, dash='dash'),
        xref='x',
        yref='y',
             )
             )

    fig3.add_shape(
    go.layout.Shape(
        type='line',
        x0=league_avg_values2['Matches played'], 
        y0=y_min_cs,
        x1=league_avg_values2['Matches played'],
        y1=y_max_cs,
        line=dict(color='blue', width=1, dash='dash'),
        xref='x',
        yref='y',
              )
           )
    fig3.update_traces(textposition='top center')
    fig3.update_traces(marker=dict(size=8))
    # for annotation in fig3.layout.annotations:
    #          if 'variable=' in annotation.text:
    #                     annotation.text = annotation.text.split('=')[1]
    
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
    if not AI21_api_key or not api_token:
        st.error("Please provide both the TOGETHER API Key and the API Key.")
    else:
        try:
            # Initialize the LLM model
            llm = ChatAI21(
                 model="jamba-instruct-preview",
#     base_url="https://api.aimlapi.com/chat/completions",
                 api_key=AI21_api_key,
                 max_tokens=4096,
                 temprature=0.7,
                 top_p=1,
                 stop=[],
                  )

        # Loading document through loader
            loader = CSVLoader("GK_ElginFC.csv", encoding="windows-1252")
            docs = loader.load()
        # st.write("Documents loaded successfully.")
  
        # Initialize HuggingFaceHubEmbeddings with the provided API token
            embedding = HuggingFaceHubEmbeddings(huggingfacehub_api_token=api_token)
        # st.write("HuggingFaceHubEmbeddings initialized successfully.")

        # Initialize Chroma vector store
            try:
                vectorstore = FAISS.from_documents(documents=docs, embedding=embedding)
                retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 103, 'fetch_k': 103})
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

###################################################### Full Back #############################################  
elif position == 'FB':
    df_position = pvt_df_FB

    original_metrics =[
       'Successful defensive actions per 90', 'Defensive duels per 90',
       'Defensive duels won, %', 'Aerial duels per 90', 'Aerial duels won, %',
       'Interceptions per 90', 'Crosses per 90', 'Accurate crosses, %',
       'Accurate forward passes, %', 'Accurate long passes, %',
       'Passes to final third per 90', 'Accurate passes to final third, %']
    weights=[1,1,1,0.8,0.8,1,0.9,1,0.9,1,0.9,1]
    weighted_metrics = pd.DataFrame()
    for metric, weight in zip(original_metrics, weights):
        weighted_metrics[metric] = df_position[metric] * weight
    
    # Calculate z-scores for the weighted metrics
    z_scores = pd.DataFrame()
    for metric in original_metrics:
        mean = weighted_metrics[metric].mean()
        std = weighted_metrics[metric].std()
        z_scores[f'{metric} zscore'] = (weighted_metrics[metric] - mean) / std

# Aggregate the z-scores to get a final z-score
    df_position["FB zscore"] = z_scores.mean(axis=1)

# Calculate final z-score and score
    original_mean = df_position["FB zscore"].mean()
    original_std = df_position["FB zscore"].std()
    df_position["FB zscore"] = (df_position["FB zscore"] - original_mean) / original_std
    df_position["FB Score(0-100)"] = (norm.cdf(df_position["FB zscore"]) * 100).round(2)
    df_position['Player Rank'] = df_position['FB Score(0-100)'].rank(ascending=False)

    # df_position["defensive zscore"] = np.dot(df_position[original_metrics], weights)
    # original_mean = df_position["defensive zscore"].mean()
    # original_std = df_position["defensive zscore"].std()
    # df_position["defensive zscore"] = (df_position["defensive zscore"] - original_mean) / original_std
    # df_position["Defender Score(0-100)"] = (norm.cdf(df_position["defensive zscore"]) * 100).round(2)
    # df_position['Player Rank'] = df_position['Defender Score(0-100)'].rank(ascending=False)
    # Dropdown menu for player selection based on position
    if st.sidebar.button('Show Top 5 Players'):
        df_position_reset = df_position.reset_index()
        df_position_sorted = df_position_reset.sort_values(by='FB Score(0-100)', ascending=False)  # Assuming higher score is better

# Remove duplicates, keeping the one with the highest 'Defender Score(0-100)'
        df_position_unique = df_position_sorted.drop_duplicates(subset='Player', keep='first')

# Step 2: Get the top 5 players
        top_5_df = df_position_unique.head(5) 
        # Extract top 5 player names and their unique identifiers
        top_5_players = top_5_df[['Player', 'FB Score(0-100)']].set_index('Player').to_dict()['FB Score(0-100)']
        top_5_player_names = list(top_5_players.keys())
    
    # Multiselect only includes top 5 players
        players_FB = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
        df_filtered2 = df_position_reset[df_position_reset['Player'].isin(players_FB)]
    
    # To ensure only the best rank is retained for each player
        df_filtered2 = df_filtered2.sort_values(by='FB Score(0-100)', ascending=False)
        df_filtered2 = df_filtered2.drop_duplicates(subset='Player', keep='first')

    else:
    # Multiselect includes all players
        players_FB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
        df_filtered = df_position.loc[players_FB]
        df_filtered2=df_filtered.reset_index()

    # players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    # df_filtered = df_position.loc[players_FB]
    df_filtered_new=df_position.reset_index()
    df_filtered_new['Defensive duels won per 90'] = df_filtered_new['Defensive duels per 90'] * (df_filtered_new['Defensive duels won, %'] / 100)
    df_filtered_new['Aerial duels won per 90'] = df_filtered_new['Aerial duels per 90'] * (df_filtered_new['Aerial duels won, %'] / 100)
    league_avg_row = df_filtered_new[df_filtered_new['Player'] == 'League Two Average']

# Extract league average values
    league_avg_values = {
    'Successful defensive actions per 90': league_avg_row['Successful defensive actions per 90'].values[0],
    'Defensive duels won per 90': league_avg_row['Defensive duels won per 90'].values[0],
    'Interceptions per 90': league_avg_row['Interceptions per 90'].values[0],
    'Aerial duels won per 90': league_avg_row['Aerial duels won per 90'].values[0]
      }
# get max value for X and Y to create quadrants
    x_max = df_filtered_new['Successful defensive actions per 90'].max()
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

    df_filtered2 = df_filtered2.rename(columns={'Successful defensive actions per 90': 'Successful def. Action/90'})
   

    df_filtered2['Defensive duels won per 90'] = df_filtered2['Defensive duels per 90'] * (df_filtered2['Defensive duels won, %'] / 100)
    df_filtered2['Aerial duels won per 90'] = df_filtered2['Aerial duels per 90'] * (df_filtered2['Aerial duels won, %'] / 100)
    # df_filtered2 = df_filtered2.rename(columns={'Successful defensive actions per 90': 'Successful def. Action/90'})

   
    fig = px.scatter(df_filtered2, x='Successful def. Action/90', y=['Defensive duels won per 90', 'Interceptions per 90', 'Aerial duels won per 90'], facet_col='variable',
                facet_col_spacing=0.08,  color='Player',  title='Defensive Action')

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
            x0=league_avg_values['Successful defensive actions per 90'],
            y0=y_min_values[facet_name],
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
    df_position2=df_filtered2.drop(columns=[ 'FB zscore','FB Score(0-100)','Player Rank','Team','Contract Expiry \n(Trnsfmkt)','Age',
                        'Matches played','Minutes played'])
                              
    radar_fig =create_radar_chart(df_position2.set_index('Player'), players_FB, id_column='Player', title=f'Radar Chart for Selected {position} Players and League Average')
    # st.pyplot(radar_fig)
    columns_to_display = ['Player','Team','Age', 'Matches played', 'Minutes played', 'FB Score(0-100)', 'Player Rank']
    df_filtered_display=df_filtered2
    df_filtered_display = df_filtered_display[columns_to_display].rename(columns={
      'FB Score(0-100)': 'Rating (0-100)',
      'Matches played': 'Matches played (2023/24)'
         })
    df_filtered_display = df_filtered_display.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

# Style the DataFrame
    def style_dataframe(df):
        return df.style.set_table_styles(
        [
            {"selector": "thead th", "props": [("font-weight", "bold"), ("background-color", "#4CAF50"), ("color", "white")]},
            {"selector": "td", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
            {"selector": "table", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
        ]
          ).hide(axis="index")

    styled_df = style_dataframe(df_filtered_display)

# Display styled DataFrame in Streamlit
    # st.write("Players Info:")
    # st.dataframe(styled_df, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(radar_fig)
    with col2:
        st.write("Players Info:")
        st.dataframe(styled_df, use_container_width=True)

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

    df_filtered2 = df_filtered2.sort_values(by='Accurate crosses, %', ascending=False)

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered2.melt(id_vars='Player', value_vars=['Accurate crosses, %'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Value', y='Player', color='Metric', orientation='h', title=f'{position} Crossing Skills')
    st.plotly_chart(fig3)
    

    # col1, col2 = st.columns([1.5, 1])
    # with col1:
    #     st.plotly_chart(fig2)
    # with col2:
    #     st.plotly_chart(fig3)
    # Input field for user prompt
    # user_prompt = st.text_input("Enter your query:")
    if not AI21_api_key or not api_token:
        st.error("Please provide both the TOGETHER API Key and the API Key.")
    else:
        try:
            # Initialize the LLM model
            llm = ChatAI21(
                 model="jamba-instruct-preview",
#     base_url="https://api.aimlapi.com/chat/completions",
                 api_key=AI21_api_key,
                 max_tokens=4096,
                 temprature=0.7,
                 top_p=1,
                 stop=[],
                  )

        # Loading document through loader
            loader = CSVLoader("FB_ElginFC.csv", encoding="windows-1252")
            docs = loader.load()
        # st.write("Documents loaded successfully.")
  
        # Initialize HuggingFaceHubEmbeddings with the provided API token
            embedding = HuggingFaceHubEmbeddings(huggingfacehub_api_token=api_token)
        # st.write("HuggingFaceHubEmbeddings initialized successfully.")

        # Initialize Chroma vector store
            try:
                vectorstore = FAISS.from_documents(documents=docs, embedding=embedding)
                retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 123, 'fetch_k': 123})
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

###################################################### Center Attacking Midfielder #############################################  
elif position == 'CAM':
    df_position = pvt_df_CAM

    original_metrics =[
       'Assists', 'Defensive duels per 90',
       'Defensive duels won, %', 'Successful attacking actions per 90',
       'Shots per 90', 'Shots on target, %', 'Successful dribbles, %',
       'Offensive duels won, %', 'Progressive runs per 90',
       'Received passes per 90', 'Passes per 90', 'Accurate passes, %',
       'Accurate forward passes, %', 'Accurate passes to final third, %',
       'Accurate passes to penalty area, %', 'Accurate progressive passes, %']
    weights=[1,0.8,0.8,1,0.9,0.9,0.8,1,1,1,1,1,1,1,1,1]
    weighted_metrics = pd.DataFrame()
    for metric, weight in zip(original_metrics, weights):
        weighted_metrics[metric] = df_position[metric] * weight
    
    # Calculate z-scores for the weighted metrics
    z_scores = pd.DataFrame()
    for metric in original_metrics:
        mean = weighted_metrics[metric].mean()
        std = weighted_metrics[metric].std()
        z_scores[f'{metric} zscore'] = (weighted_metrics[metric] - mean) / std

# Aggregate the z-scores to get a final z-score
    df_position["CAM zscore"] = z_scores.mean(axis=1)

# Calculate final z-score and score
    original_mean = df_position["CAM zscore"].mean()
    original_std = df_position["CAM zscore"].std()
    df_position["CAM zscore"] = (df_position["CAM zscore"] - original_mean) / original_std
    df_position["CAM Score(0-100)"] = (norm.cdf(df_position["CAM zscore"]) * 100).round(2)
    df_position['Player Rank'] = df_position['CAM Score(0-100)'].rank(ascending=False)

    # df_position["defensive zscore"] = np.dot(df_position[original_metrics], weights)
    # original_mean = df_position["defensive zscore"].mean()
    # original_std = df_position["defensive zscore"].std()
    # df_position["defensive zscore"] = (df_position["defensive zscore"] - original_mean) / original_std
    # df_position["Defender Score(0-100)"] = (norm.cdf(df_position["defensive zscore"]) * 100).round(2)
    # df_position['Player Rank'] = df_position['Defender Score(0-100)'].rank(ascending=False)
    # Dropdown menu for player selection based on position
    if st.sidebar.button('Show Top 5 Players'):
        top_5_players = df_position.nsmallest(5, 'Player Rank').index.tolist()
    # Multiselect only includes top 5 players
        players_CAM = st.sidebar.multiselect('Select players:', options=top_5_players, default=top_5_players)
    else:
    # Multiselect includes all players
        players_CAM = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])

    # players_CB = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    df_filtered = df_position.loc[players_CAM]
    
    # players_CF = st.sidebar.multiselect('Select players:', options=df_position.index.tolist(), default=['League Two Average'])
    # df_filtered = df_position.loc[players_CF]

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
    

    # Create radar chart for selected players
    df_position2=df_filtered.drop(columns=[ 'Team','Contract Expiry \n(Trnsfmkt)',
                        'Matches played', 'Minutes played','Age',
                       'CF Score(0-100)', 'Player Rank', 'CF zscore'])
                              
    radar_fig =create_radar_chart(df_position2, players_CAM, id_column='Player', title=f'Radar Chart for Selected {position} Players and League Average')
    
    columns_to_display = ['Player','Team','Age', 'Matches played', 'Minutes played', 'CAM Score(0-100)', 'Player Rank']
    df_filtered_display=df_filtered.reset_index()
    df_filtered_display = df_filtered_display[columns_to_display].rename(columns={
      'CAM Score(0-100)': 'Rating (0-100)',
      'Matches played': 'Matches played (2023/24)'
         })
    df_filtered_display = df_filtered_display.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

# Style the DataFrame
    def style_dataframe(df):
        return df.style.set_table_styles(
        [
            {"selector": "thead th", "props": [("font-weight", "bold"), ("background-color", "#4CAF50"), ("color", "white")]},
            {"selector": "td", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
            {"selector": "table", "props": [("background-color", "#f2f2f2"), ("color", "black")]},
        ]
          ).hide(axis="index")

    styled_df = style_dataframe(df_filtered_display)

# Display styled DataFrame in Streamlit
    # st.write("Players Info:")
    # st.dataframe(styled_df, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(radar_fig)
    with col2:
        st.write("Players Info:")
        st.dataframe(styled_df, use_container_width=True)
    

    
    
    
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

    # Melt the dataframe to long format for stacking
    df_melted = df_filtered3.melt(id_vars='Player', value_vars=['Successful attacking actions per 90', 'xG per 90','Goals per 90'], var_name='Metric', value_name='Value')

    # Create stacked bar chart
    fig3 = px.bar(df_melted, x='Value', y='Player', color='Metric', orientation='h', title=f'{position} Attacking threats')
    st.plotly_chart(fig3)

    
    # Input field for user prompt
    # user_prompt = st.text_input("Enter your query:")
    if not AI21_api_key or not api_token:
        st.error("Please provide both the TOGETHER API Key and the API Key.")
    else:
        try:
            # Initialize the LLM model
            llm = ChatAI21(
                 model="jamba-instruct-preview",
#     base_url="https://api.aimlapi.com/chat/completions",
                 api_key=AI21_api_key,
                 max_tokens=4096,
                 temprature=0.7,
                 top_p=1,
                 stop=[],
                  )

        # Loading document through loader
            loader = CSVLoader("CAM_ElginFC.csv", encoding="windows-1252")
            docs = loader.load()
        # st.write("Documents loaded successfully.")
  
        # Initialize HuggingFaceHubEmbeddings with the provided API token
            embedding = HuggingFaceHubEmbeddings(huggingfacehub_api_token=api_token)
        # st.write("HuggingFaceHubEmbeddings initialized successfully.")

        # Initialize Chroma vector store
            try:
                vectorstore = FAISS.from_documents(documents=docs, embedding=embedding)
                retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 103, 'fetch_k': 103})
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



