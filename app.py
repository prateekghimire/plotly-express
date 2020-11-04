from flask import Flask, render_template
import pandas as pd
import plotly as py
import plotly.express as px #For high level data visualization
url='https://covid.ourworldindata.org/data/owid-covid-data.csv'
data=pd.read_csv(url)
pd.options.display.float_format = '{:.2f}'.format #getting rid of 'e'form in data value

data_countrydate = data[data['new_cases']>0]
data_countrydate=data_countrydate.groupby(['date','location']).sum().reset_index()
fig = px.choropleth(data_countrydate, 
                    locations="location", 
                    locationmode = "country names",
                    color="new_cases", 
                    hover_name="location", 
                    animation_frame="date"
                   )
fig.update_layout(
    title_text = 'Spread of Coronavirus',
    title_x = 0.5,
    geo=dict(
        showframe = False,
        showcoastlines = False,
    ))

py.offline.plot(fig,filename='templates/worldcases.html',auto_open=False)




Nepal_data=data[data.location=='Nepal']
Nepal_data=Nepal_data.groupby(by='date').sum().reset_index()
Nepal_data=Nepal_data[Nepal_data.new_cases>0]
Nepal_data['country']='Nepal'

line_chart=px.line(Nepal_data,y='total_cases',x='date',hover_name='country', labels={'total_cases':'Total Cases','date':'Date'})
line_chart.update_layout(title_text='Nepal covid spread')
py.offline.plot(line_chart,filename='templates/nepaltotalcases.html',auto_open=False)

line_chart=px.line(Nepal_data,y='total_deaths',x='date',hover_name='country', labels={'total_deaths':'Total Deaths','date':'Date'})
line_chart.update_layout(title_text='Covid Deaths')
py.offline.plot(line_chart,filename='templates/nepaltotaldeaths.html',auto_open=False)

line_chart=px.line(Nepal_data,y='positive_rate',x='date',hover_name='positive_rate', labels={'positive_rate':'Positive Rate','date':'Date'})
line_chart.update_layout(title_text='Positive Test Rate')
py.offline.plot(line_chart,filename='templates/nepalpositivetestrate.html',auto_open=False)

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/world')
def world():
    return render_template('worldcases.html')

@app.route('/nepaltotalcases')
def total_cases():
    return render_template('nepaltotalcases.html')

@app.route('/nepaltotaldeaths')
def total_deaths():
    return render_template('nepaltotaldeaths.html')

@app.route('/nepalpositivetestrate')
def positive_rate():
    return render_template('nepalpositivetestrate.html')

#app.run(debug=True)