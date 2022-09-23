#!/usr/bin/env python3 

from ast import Bytes
import tweepy
from twit_img_secrets import *
import re
from PIL import Image
from io import BytesIO
import requests

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

from collections import namedtuple

mediaMetadata = namedtuple('mediaMetadata', 'n w h url_sz url_orig fn ext')

class TwitImgDL():
	_regex=re.compile('https://([^/]+)/([^/]+)/status/([0-9]+)')
	def __init__(self, url=None, username=None, tweet_num_id=None,
		fn_text_str='untitled'):
		self._url = url
		self._user = username
		self._n_id = tweet_num_id
		self.fn_text_str = fn_text_str
		self.media = []
		self.media = []
		if url != None:
			self._parseURL()
		else:
			self._makeURL()

	def _parseURL(self):
		match_obj = self._regex.match(self.url)
		self._user = match_obj.group(2)
		self._n_id = int(match_obj.group(3))
	def _makeURL(self):
		if self._user != None and self._n_id != None:
			self._url = 'https://twitter.com/{}/status/{}'.format(
				self._user, self._n_id
			)

	@property
	def url(self):
		return self._url
	@url.setter
	def url(self, url):
		self._url = url
		self._parseURL()

	@property
	def username(self):
		return self._user
	@username.setter
	def username(self, username):
		self._user = username
		self._makeURL()

	@property
	def tweet_num_id(self):
		return self._n_id
	@tweet_num_id.setter
	def tweet_num_id(self, tweet_num_id):
		self._n_id = tweet_num_id
		self._makeURL()

	def scan(self, api=tweepy.API(auth)):
		if len(self.media) > 0:
			return self.media
		resp = api.get_status(self._n_id)
		
		hasMedia = 'media' in resp.extended_entities.keys()
		if hasMedia:
			media_list=resp.extended_entities['media']
		else:
			assert "not hasMedia"

		# Now get the largest ones.

		for imx,mx in enumerate(media_list):
			saved={'w':-1,'h':-1,'name':None}
			for sz in mx['sizes']:
				if mx['sizes'][sz]['w'] > saved['w'] or mx['sizes'][sz]['h'] > saved['h']:
					saved['w'] = mx['sizes'][sz]['w']
					saved['h'] = mx['sizes'][sz]['h']
					saved['name'] = sz
			#print(" Largest {} x {}".format(saved['w'], saved['h']))
			img_url_known = "{}?name={}".format(mx['media_url'], saved['name'])
			img_url_orig = "{}?name={}".format(mx['media_url'], 'orig')
			#print(' URL: \'{}\''.format(img_url))

			fn = "Tw '{}'{} by {} {}".format(
				self.fn_text_str,
				'-{}'.format(imx+1) if len(media_list) > 1 else '',
				resp.author.screen_name,
				resp.created_at.strftime('%Y-%m-%d'),
			)

			self.media.append(
				mediaMetadata(imx+1, saved['w'], saved['h'], 
					img_url_known, img_url_orig, fn, mx['media_url'][-3:]),
			)
		return self.media

	@classmethod
	def download(cls, m, dl_dir):
		print("Fetching '{}'".format(m.url_orig))
		# First try to get the "original" image
		resp = requests.get(m.url_orig)
		valid=False
		if resp.status_code == 200:
			# keep trying
			h_img = Image.open(BytesIO(resp.content))
			if h_img.size[0] >= m.w and h_img.size[1] >= m.h:
				# This is bigger than the other one, use it!
				sz = h_img.size
				dat = resp.content
				valid = True
				url_used = m.url_orig

		if not valid:
			resp = requests.get(m.url_sz)
			sz = (m.w, m.h)
			dat = resp.content
			url_used = m.url_sz

		fn_full = '{} {}x{}.{}'.format(m.fn, sz[0], sz[1], m.ext)
		fn_loc = '{}/{}'.format(dl_dir, fn_full)
		print("Saving '{}' to {}".format(m.fn, dl_dir))
		print("   size: {}x{}".format(sz[0], sz[1]))
		with open(fn_loc, 'wb') as img:
			img.write(resp.content)
		
		img_ret={
			'url': url_used,
			'fn': fn_full,
			'path': fn_loc
		}

		return img_ret
		
if __name__ == "__main__":
	from os import makedirs

	n_id = 1254209651836502016
	user = 'vupl4'
	
	user = 'aokarimero'
	n_id = 1288066770905915392
	url = 'https://twitter.com/{}/status/{}'.format(user,n_id)

	#n_id = 1255252210331660292
	#user = 'sixveeceear'
	#tw_text_str = 'blueart from 2018'

	url = 'https://twitter.com/tatami111/status/1304361594667761664'
	url = 'https://twitter.com/novelance/status/1425283150410752003'
	url = 'https://twitter.com/uyjpn/status/1572514801162817538'

	ob = TwitImgDL(url)
	ob.fn_text_str = 'untitled_1'
	ob.scan()

	dl_dir = 'imgs'
	makedirs(dl_dir, exist_ok=True)

	for m in ob.media:
		TwitImgDL.download(m, dl_dir)
