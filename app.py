# -*- coding: utf-8 -*-
"""
Created on Fri May 20 12:53:35 2016

@author: jnara
"""

from __future__ import print_function

from flask import Flask,render_template, request

# For Bokeh
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8


import pandas as pd

# For time stamps
from datetime import datetime

import os
import requests
project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=template_path)


# Set up End and Start times for data grab
end = datetime.now()
start = datetime(end.year,end.month-1,end.day)

@app.route('/',methods=['GET'])
def home():
    return render_template("home.html")
@app.route('/graph',methods=['GET', 'POST'])
def graph():
    # request was a POST
    StockTicker = request.form['stock']
    Type = request.form['type']
        
    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % StockTicker
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    json_dat = raw_data.json()
    data = json_dat["data"]
    df = pd.DataFrame(data, columns= json_dat["column_names"])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df["Date"] >= start]
    p1 = figure(x_axis_type = "datetime")
    p1.title = "Stock Closing Prices"
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'    
    p1.line(df["Date"], df[Type], color='#A6CEE3', legend=StockTicker)
        
    
    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/user_guide/embedding.html#components      
    script, div = components(p1, INLINE)
        
    return encode_utf8(render_template('graph.html', script=script, div=div))


if __name__ == "__main__":
    app.run(port=33507)