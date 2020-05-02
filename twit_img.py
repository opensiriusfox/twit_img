#!/usr/bin/env python3 

import tweepy
import requests
from twit_img_secrets import *
from os import makedirs

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)


dl_dir = 'imgs'
makedirs(dl_dir, exist_ok=True)

n_id = 1254209651836502016
user = 'vupl4'
tw_text_str = 'untitled'

#n_id = 1255252210331660292
#user = 'sixveeceear'
#tw_text_str = 'blueart from 2018'

url = 'https://twitter.com/{}/status/{}'.format(user,n_id)

r = api.get_status(n_id)

hasMedia = 'media' in r.extended_entities.keys()
if hasMedia:
	m=r.extended_entities['media']
else:
	assert "not hasMedia"


print(
	"Tweet by: '{}' @{}\n".format(r.author.name, r.author.screen_name),
	"On: {}\n".format('none'),
	"Media: {}\n".format(hasMedia)
	)

saved={'w':-1,'h':-1,'name':None}
for imx,mx in enumerate(m):
	for sz in mx['sizes']:
		if mx['sizes'][sz]['w'] > saved['w'] or mx['sizes'][sz]['h'] > saved['h']:
			saved['w'] = mx['sizes'][sz]['w']
			saved['h'] = mx['sizes'][sz]['h']
			saved['name'] = sz
	print(" Largest {} x {}".format(saved['w'], saved['h']))
	img_url = "{}?name={}".format(mx['media_url'], saved['name'])
	print(' URL: \'{}\''.format(img_url))

	#tw_text_str = str(n_id)

	fn = "Tw '{}'{} by {} {} {}x{}.{}".format(
		tw_text_str,
		'-{}'.format(imx+1) if len(m) > 1 else '',
		r.author.screen_name,
		r.created_at.strftime('%Y-%m-%d'),
		saved['w'], saved['h'],
		mx['media_url'][-3:]
	)

	print("Fetching '{}'".format(img_url))
	resp = requests.get(img_url)
	fn_loc = '{}/{}'.format(dl_dir, fn)
	print("Saving '{}' to ".format(fn, dl_dir))
	with open(fn_loc, 'wb') as img:
		img.write(resp.content)
	print(fn)