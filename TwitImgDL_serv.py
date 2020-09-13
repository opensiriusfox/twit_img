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


app = Flask(__name__)
app.config['SECRET_KEY'] = \
	b'\xaf|a`\xa1\x034@\x0f4J\xd4F\x89\x98\x15\x9c\x92' + \
	b'\xd1\x96\x05\xbcu\r\xa5N6o\xa9\x12\x98\xe3'

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
		print("Fetching '{}'".format(m.url))
		resp = requests.get(m.url)
		fn_loc = '{}/{}'.format(dl_dir, m.fn)
		print("Saving '{}' to {}".format(m.fn, dl_dir))
		with open(fn_loc, 'wb') as img:
			img.write(resp.content)

		imgs.append({
			'url': m.url,
			'fn': m.fn,
			'path': fn_loc
		})

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
			attachment_filename='')

