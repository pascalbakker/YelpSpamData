from recommend import app
from flask import request,Flask,redirect,url_for,render_template
from recommend.recommendation import do_recommendation

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/recommend', methods=["POST","GET"])
def recommend():
    if request.method =="POST":
        texts = request.form["tf"]
        return redirect(url_for("hotel",query = texts))
    elif request.method =="GET":
        return render_template("index.html")

@app.route('/hotel/<query>')
def hotel(query):
    recommendations= do_recommendation(query)
    return render_template("hotel.html",query=query,tables= recommendations.to_numpy())

@app.route('/report')
def report():
    return render_template("ourproject.html")

if __name__ == '__main__':
# Map command line arguments to function arguments.
    app.run(host='127.0.0.1',port='8080',debug=True)