from flask import Flask, render_template

app=Flask(__name__,template_folder='template')


@app.route('/plot/',methods =["GET", "POST","DELETE"])
def gfg():
    from flask import request 
    if request.method == "POST" or "GET":
        code = request.form.get("ccode")
    return render_template("plot.html")


@app.route('/plot/plotfinal',methods =["GET", "POST","DELETE"])
def plot():
    from flask import request
    from pandas_datareader import data
    import datetime
    from datetime import date
    import bokeh.plotting as bp
    from bokeh.models.annotations import Title
    from bokeh.embed import components
    from bokeh.resources import CDN
    
    code = request.form.get("ccode")
    start=datetime.datetime(2019,12,3)
    end=datetime.datetime(2020,12,13)
    df=data.DataReader(name=code.upper(),data_source="yahoo",start=start,end=end) #Reliance
    print(df)
    p=bp.figure(x_axis_type='datetime',width=1200, height=500)
    title_text=Title()
    title_text.text = code.upper()
    p.title=title_text
    hours_12=12*60*60*1000

    def inc_dec(c,o):
        if c>o:
            value="Increase"
        elif c==o:
            value="Equal"
        else:
            value="Decrease"
        return value
    df["Status"]=[inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Close-df.Open)
    p.segment(df.index, df.High,df.index,df.Low,color="black")
    p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"], hours_12, df.Height[df.Status=="Increase"],fill_color='#73ffff',line_color='black')
    p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"], hours_12, df.Height[df.Status=="Decrease"],fill_color='#eb1438',line_color='black')
    script1,div1=components(p)
    cdn_js=CDN.js_files[0]
    return render_template("plotfinal.html",script1=script1,div1=div1,cdn_js=cdn_js)
   
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
 
