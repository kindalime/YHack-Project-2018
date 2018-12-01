from flask import Flask, jsonify, request
import os
import random

app = Flask(__name__)

from app import routes