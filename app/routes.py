from flask import Blueprint
from flask import Flask, render_template,request
import plotly
import plotly.graph_objs as go
from plotly.offline import  plot
import pathlib
import pandas as pd
import numpy as np
import json

from flask import redirect, url_for, render_template, request, jsonify, make_response, flash
Neosum = Blueprint('Neosum',__name__)


def data_used():
    # Import data
    df = pd.read_csv(
        "C:\\Users\\lmumelo\\OneDrive - Kemri Wellcome Trust\\app\\flask-dashboard-adminator-master\\data\\fullredcap.csv", low_memory=False)
    return df

#####################################################################################
def create_df():
    # get counts per NAR type
    df_nar = pd.DataFrame(data_used().groupby('Hospital_id')['Document Source'].value_counts())
    df_nar = df_nar.rename({'Document Source': 'Doc count'}, axis='columns')
    df_nar = df_nar.reset_index()

    return df_nar



def create_plot(df_nar):
    # set up plotly figure
    fig = go.Figure()
    # Manage NAR types (who knows, there may be more types with time?)
    nars = df_nar['Document Source'].unique()
    nars = nars.tolist()
    nars.sort(reverse=False)
    # add one trace per NAR type and show counts per hospital
    data = []
    for nar in nars:
        # subset dataframe by NAR type
        df_ply = df_nar[df_nar['Document Source'] == nar]

        # add trace
        fig.add_trace(go.Bar(x=df_ply['Hospital_id'], y=df_ply['Doc count'], name='Document Type=' + str(nar)))

    # make the figure a bit more presentable
    fig.update_layout(title='Document Use per hospital',
                      yaxis=dict(title='<i>count of Docuement types</i>'),
                      xaxis=dict(title='<i>Hospital</i>'),autosize=False,)

    graphe = plot(fig,config={"displayModeBar": False},
                  show_link=False, include_plotlyjs=False,
                  output_type='div')


    #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphe

@Neosum.route('/')
def index():

    bar = create_plot(create_df())
    return render_template('index.html', plot=bar)
