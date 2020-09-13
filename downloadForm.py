#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class downloadForm(FlaskForm):
	url = StringField('URL', validators=[DataRequired()])
	submit = SubmitField('Download')