from flask import Flask
from helpers.config import Config

app = Flask(__name__, template_folder="./app/templates", static_folder="./app/static")
app.config.from_object(Config)

from app import views