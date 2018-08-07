from flask import Flask
from helpers.config import Config

app = Flask(__name__, template_folder="./grandpy/templates", static_folder="./grandpy/static")
app.config.from_object(Config)

from grandpy import views