#!/usr/bin/env python3

from TwitImgDL import TwitImgDL
from os import makedirs
import io
import requests

from flask import Flask
from flask import render_template
from flask import request
from flask import send_file

from downloadForm import downloadForm

# Flask secret is some random key.
# python -c 'import os; print(os.urandom(16))'
from twit_img_secrets import flask_secret


app = Flask(__name__)
app.config['SECRET_KEY'] = flask_secret

dl_dir = 'imgs'
makedirs(dl_dir, exist_ok=True)

@app.route("/")
def index():
	form = downloadForm()
	return render_template('form_data.html', form=form)

@app.route("/redir", methods=['POST'])
def redirect():
	if request.method != 'POST':
		pass
		# redirect back to main page?
	
	ob = TwitImgDL(request.form['url'])
	ob.fn_text_str = 'untitled_1'
	ob.scan()

	imgs = []

	for m in ob.media:
		imgs.append(TwitImgDL.download(m, dl_dir))

	return render_template('preview.html', imgs=imgs)

@app.route("/img/<user>/<n_id>/<extra>")
def process(user,n_id,extra):
	return "{}<br>\n{}<br>\n{}".format(user,n_id,extra)

@app.route("/{}/<image_file>".format(dl_dir))
def serve_image(image_file):
	fn_loc = '{}/{}'.format(dl_dir ,image_file.replace('/',''))
	with open(fn_loc, 'rb') as bin_img:
		return send_file(
			io.BytesIO(bin_img.read()),
			download_name=image_file)

