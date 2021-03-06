#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration 
    Bot used : BookFlight-SDK
    """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LuisAppId", "ea02289f-c445-454b-a2be-76deca160a9d")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "2246a01e45d447ceb6f9799e72a75504")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westeurope.api.cognitive.microsoft.com")
