#!/usr/bin/env python3

from TwitImgDL import TwitImgDL
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
	url = {'URL': ''}
	return render_template('index.html', title='Home', url=url)