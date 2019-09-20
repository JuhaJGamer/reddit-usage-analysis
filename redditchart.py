#!/usr/bin/env python3
import plotly.graph_objects as go
import pandas
import argparse
import csv
import datetime

parser = argparse.ArgumentParser(description='Visualize analysis of trends in reddit usage')
parser.add_argument('file',type=argparse.FileType('r'),help='CSV to chart"')
parser.add_argument('-a','--average-only',action='store_true',help='Only show average values',default=False)
parser.add_argument('-e','--exact-only',action='store_true',help='Only show exact values',default=False)
args = parser.parse_args()

df = {}
ls = []
reader = csv.reader(args.file,dialect="unix")
for row in reader:
    print(row)
    if len(ls) is 0:
        for name in row:
            df[name] = []
            ls.append(name)
        continue
    df[ls[0]].append(datetime.datetime.strptime(row[0],"%Y-%m-%d"))
    for i in range(1,len(row)):
        try:
                df[ls[i]].append(float(row[i]))
        except ValueError:
            df[ls[i]].append(0)

fig = go.Figure()
fig_fill = 'tozeroy'
for column in range(1,len(ls)):
    print(ls[column])
    if(args.average_only):
        if "day average" not in ls[column]:
            continue
    elif (args.exact_only):
        if "day average" in ls[column]:
            continue
    fig.add_trace(go.Scatter(x=df["Time"],y=df[ls[column]],fill=fig_fill,name=ls[column]))
    fig_fill='tozeroy'
fig.show()

