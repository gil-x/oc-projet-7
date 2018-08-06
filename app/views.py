#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import request, render_template, jsonify
# import json

import os
from run import app
from helpers.grandpybot import GrandPyBot
from helpers.forms import MessageForm
from helpers.config import Config


@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def home():
    form = MessageForm()
    print("Config.API_KEY:", Config.API_KEY)
    print("Config.SECRET_KEY:", Config.SECRET_KEY)
    print("os.environ.get('GOOGLE_API_KEY'):", os.environ.get('GOOGLE_API_KEY'))
    return render_template('home.html', title="GrandPyBot", form=form, API_KEY=os.environ.get('GOOGLE_API_KEY'))

@app.route('/message/', methods=['POST'])
def grandpy(message="spam"):
    form = MessageForm()
    grandpy = GrandPyBot()

    if form.validate_on_submit():
        print("===\n@app.route|grandpy: valid submission\n===")
        message = form.message.data
        return jsonify(grandpy.ask(message))
    else:
        print("===\n@app.route|grandpy: submission is not valid\n===")
        return "Hein ?"

if __name__ == '__main__':
    app.run(debug=True)
