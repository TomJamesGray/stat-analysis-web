import argparse
import logging
from stat_analysis.datasets import csv_dataset
from flask import Flask
from flask import render_template

logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")