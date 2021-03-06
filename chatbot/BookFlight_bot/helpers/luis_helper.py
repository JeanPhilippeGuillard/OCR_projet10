# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from booking_details import BookingDetails


class Intent(Enum):
    BOOK_FLIGHT = "BookFlight"
    CONFIRM = "Confirm"
    GREETINGS = "Greetings"
    CANCEL = "Cancel"
    NONE_INTENT = "NoneIntent"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.BOOK_FLIGHT.value:
                result = BookingDetails()

                # We need to get the result from the LUIS JSON which at every level returns an array.

                # Departure location
                departure_location_entities = recognizer_result.entities.get("$instance", {}).get(
                    "departure_location", []
                )
                if len(departure_location_entities) > 0:
                    result.origin = departure_location_entities[0]["text"].capitalize()


                # Return location
                return_location_entities = recognizer_result.entities.get("$instance", {}).get(
                    "return_location", []
                )
                if len(return_location_entities) > 0:
                    result.destination = return_location_entities[0]["text"].capitalize()
  

                # These values will be a TIMEX. And we are only interested in a Date so grab the first result and drop
                # the Time part. TIMEX is a format that represents DateTime expressions that include some ambiguity.
                # e.g. missing a Year.

                # Departure date
                departure_date_entities = recognizer_result.entities.get("datetime", []).get(
                    "departure_date", []
                )
                if departure_date_entities:
                    timex = departure_date_entities[0]["timex"]

                    if timex:
                        datetime = timex[0].split("T")[0]

                        result.departure_date = datetime

                else:
                    result.departure_date = None

                # Return date
                return_date_entities = recognizer_result.entities.get("datetime", []).get(
                    "return_date", []
                )
                if return_date_entities:
                    timex = return_date_entities[0]["timex"]

                    if timex:
                        datetime = timex[0].split("T")[0]

                        result.return_date = datetime

                else:
                    result.return_date = None

                # Budget
                budget_entities = recognizer_result.entities.get("$instance", {}).get(
                    "budget", []
                )
                if len(budget_entities) > 0:
                    result.budget = budget_entities[0]["text"].capitalize()

        except Exception as exception:
            print(exception)

        return intent, result
