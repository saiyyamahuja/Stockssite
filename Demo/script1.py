# Stocks_site/Demo/script1.py
import yfinance as yf
from flask import Flask, render_template, request, redirect, url_for
import datetime
import bokeh.plotting as bp
from bokeh.models.annotations import Title
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import HoverTool
app = Flask(__name__, template_folder='templates')


@app.route('/plot/', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        code = request.form.get("ccode")
        return redirect(url_for('plot', ccode=code))
    return render_template("plot.html")


@app.route('/plot/plotfinal', methods=["GET"])
def plot():
    code = request.args.get("ccode")

    if not code:
        return "Please enter a valid company code"

    start = datetime.datetime(2019, 12, 3)
    end = datetime.datetime(2020, 12, 13)

    df = yf.download(code, start=start, end=end)

    if df.empty:
        return "Invalid stock code or no data available"
    df.columns = df.columns.get_level_values(0)
    df = df.reset_index() 

    p = bp.figure(x_axis_type='datetime', width=1200, height=500)

    title_text = Title()
    title_text.text = code.upper()
    p.title = title_text

    hours_12 = 12 * 60 * 60 * 1000 * 0.5

    def inc_dec(c, o):
        if c > o:
            return "Increase"
        elif c == o:
            return "Equal"
        else:
            return "Decrease"

    df["Status"] = df.apply(lambda row: inc_dec(row["Close"], row["Open"]), axis=1)
    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Close - df.Open)

    p.segment(df["Date"], df["High"], df["Date"], df["Low"], color="black")

    p.rect(df["Date"][df.Status == "Increase"],
        df["Middle"][df.Status == "Increase"],
        hours_12,
        df["Height"][df.Status == "Increase"],
        fill_color='#16a34a',
        line_color='black')

    p.rect(df["Date"][df.Status == "Decrease"],
        df["Middle"][df.Status == "Decrease"],
        hours_12,
        df["Height"][df.Status == "Decrease"],
        fill_color='#dc2626',
        line_color='black')

    script1, div1 = components(p)
    hover = HoverTool(tooltips=[
        ("Price", "$y")
    ])
    p.add_tools(hover)
    cdn_js = CDN.js_files[0]

    return render_template("plotfinal.html",
                           script1=script1,
                           div1=div1,
                           cdn_js=cdn_js)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about/')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)