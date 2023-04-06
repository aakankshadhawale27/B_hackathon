import os
import plotly.express as px
import pandas as pd

dir_unstr = os.listdir("D:/cloudforge/files/structured")
os.chdir("D:/cloudforge/files/structured")
dframes = []

dfTSLA = pd.read_csv("TSLA.csv")

dir_unstr = os.listdir("D:/cloudforge/files/transformed")
os.chdir("D:/cloudforge/files/transformed")

dfTweets = pd.read_csv("cleandTweets.csv")


# fig = px.line(dfTSLA, x='Date', y='High')
# fig = px.line(dfTSLA, x='Date', y='Low')

fig = px.line(dfTSLA, x='Date', y='High')
 
fig.add_scatter(x=dfTSLA['Date'], y=dfTSLA['Low'], mode='lines',name="Low" )

fig.show()

