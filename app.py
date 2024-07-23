from flask import Flask, render_template, redirect, request
from flask_session import Session
from keywordcheck import checkContent
import re

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config["DEBUG"] = True
Session(app)

@app.route('/')
def home_redirect():
    return redirect('/nl')

@app.route('/nl')
def nl():
    return render_template('nl.html')

@app.route('/nl/contentcheck')
def contentcheck():
    if request.args:
        url = request.args.get('url')
        keyword = request.args.get('keyword')
        pattern = r'^https?:\/\/'
        if re.match(pattern, url): 
            data = checkContent(keyword, url)
        else:
            data = {"error": "URL moet starten met http:// of https://"}
            return render_template('keywordcheck.html', data=data)
        return render_template('keywordcheck.html', data=data)
    return render_template('keywordcheck.html')

if __name__ == '__main__':
    app.run(debug=True)