#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

# Insight key to record logs and transfer them to Azure Insights:
INSIGHT_KEY = "bd0e01dc-2753-4227-ae8f-06fb53970148"

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LuisAppId", "6e496dfb-b657-4111-9e9d-8103daecfdd7") #FlightBooking-v1-wo-airport_list
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "2246a01e45d447ceb6f9799e72a75504")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westeurope.api.cognitive.microsoft.com")
