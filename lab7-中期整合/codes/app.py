# SJTU EE208

from flask import Flask, redirect, render_template, request, url_for
import Search_doc
import Search_img

app = Flask(__name__)

@app.route('/',methods=['GET'])
def search_doc():
    return render_template("search_doc.html")

@app.route('/im',methods=['GET'])
def search_img():
    return render_template("search_img.html")

@app.route('/result', methods=['GET'])
def result_doc():
    keyword = request.args.get('keyword')
    results = Search_doc.search(keyword)
    return render_template("result_doc.html",results=results,keyword=keyword)

@app.route('/im/result', methods=['GET'])
def result_img():
    keyword = request.args.get('keyword')
    results = Search_img.search(keyword)
    return render_template("result_img.html",results=results,keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
