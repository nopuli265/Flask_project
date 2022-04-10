from flask import Flask, render_template
from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN
app=Flask(__name__)

@app.route('/plot/')
def plot():
    start=datetime.datetime(2021,11,1)
    end=datetime.datetime(2022,3,1)

    df=data.DataReader(name='GOOG', data_source='yahoo', start=start, end=end)

    df['Middle']=(df.Open+df.Close)/2
    df['Height']=abs(df.Open-df.Close)

    def inc_dec(o,c):
        if o<c:
            value='increase'
        elif o>c:
            value='decrease'
        else:
            value='equals'
        return value
    df['Status']=[inc_dec(o,c) for o,c in zip(df.Open, df.Close)]

    p=figure(x_axis_type='datetime', width= 1000, height=300, sizing_mode='scale_width')
    p.title.text='Candlistick Chart'
    p.title.align='center'
    p.title.text_color='#ffb600'
    p.title.text_font_size='50px'
    p.title.text_font='Time'
    p.grid.grid_line_alpha=0.4

    hours_12=12*60*60*1000 # 12H = MILISECOND
    p.segment(df.index, df.High, df.index , df. Low, color='black')
    p.rect(df.index[df.Status=='increase'], df.Middle[df.Status=='increase'],hours_12, df.Height[df.Status=='increase'], 
        fill_color='#a1ff0a', line_color='black')
    p.rect(df.index[df.Status=='decrease'], df.Middle[df.Status=='decrease'],hours_12,df.Height[df.Status=='decrease'],
        fill_color='#ff0000', line_color='black')
    script1, div1= components(p)
    cdn_js=CDN.js_files[0]
    return render_template('plot.html', script1=script1, div1=div1,cdn_js=cdn_js)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/About/')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run(debug=True)
