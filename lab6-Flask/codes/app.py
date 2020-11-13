# SJTU EE208

from flask import Flask, redirect, render_template, request, url_for
import Search
app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        keyword = request.form['keyword']
        return redirect(url_for("result",keyword=keyword))
    return render_template("search.html")

@app.route('/result', methods=['GET'])
def result():
    keyword = request.args.get('keyword')
    results = Search.search(keyword)
    return render_template("result.html",results=results,keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
