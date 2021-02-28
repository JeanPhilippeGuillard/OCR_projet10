from app import app, credentials
from flask import render_template, redirect, request, url_for



#------------------------- Test instrumentation -------------------------------
import logging
from datetime import datetime
from opencensus.ext.azure.log_exporter import AzureLogHandler

INSIGHT_CONNECTION_STRING = "InstrumentationKey=" + credentials.INSIGHT_KEY

logger = logging.getLogger(__name__)

logger.addHandler(AzureLogHandler(
                    connection_string=INSIGHT_CONNECTION_STRING))

utc_time = datetime.utcnow()
logger.warning("Message d'alerte de views.py à {}".format(utc_time))
print("message d'alerte envoyé")

#---------------------------- Manage routes -----------------------------------

@app.route("/")
def home():

    return render_template("home.html")

    
