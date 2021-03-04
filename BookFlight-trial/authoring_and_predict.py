from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce

import json, time

# <AuthoringSortModelObject>
def get_child_id(model, childName):

    theseChildren = next(filter((lambda child: child.name == childName), model.children))
    
    ChildId = theseChildren.id

    return ChildId


def get_grandchild_id(model, childName, grandChildName):
    
    theseChildren = next(filter((lambda child: child.name == childName), model.children))
    theseGrandchildren = next(filter((lambda child: child.name == grandChildName), theseChildren.children))

    grandChildId = theseGrandchildren.id

    return grandChildId


def quickstart():

    # Set variables ----------------------------------------------------

    authoringKey = "2246a01e45d447ceb6f9799e72a75504"
    authoringResourceName = "jpg-luis-trial-authoring"
    predictionResourceName = "jpg-luis-trial"

    authoringEndpoint = f"https://{authoringResourceName}.cognitiveservices.azure.com/"
    predictionEndpoint = f"https://{predictionResourceName}.cognitiveservices.azure.com"


    appName = "BookFlight-SDK"
    versionId = "0.1"

    # Authenticate client------------------------------------------------

    client = LUISAuthoringClient(authoringEndpoint, CognitiveServicesCredentials(authoringKey))

    # Create LUIS application -------------------------------------------

    # define app basics
    appDefinition = {
        "name": appName,
        "initial_version_id": versionId,
        "culture": "en-us"
    }
    

    # Create app
    app_id = client.apps.add(appDefinition)
    
    # get app id - necessary for all other changes
    print(f"Created LUIS app with id {app_id}")

    # Create intention(s) ------------------------------------------------
    
    intentNames = ["BookFlight", "Confirm", "Greetings"]
    for intent in intentNames:
        client.model.add_intent(app_id, versionId, intent)

 
    # Create entity(ies) -------------------------------------------------

    # Add pre_built entity :

    client.model.add_prebuilt(app_id, versionId, prebuilt_extractor_names=["number", "money", "geographyV2", "datetimeV2"])


    # Create ML entity :
    mlEntityDefinition = [
            {
                "name": "location",
                "children": [
                    {"name": "departure_location"},
                    {"name": "return_location"}
                ]
            },
            {
                "name": "date",
                "children": [
                    {"name": "departure_date"},
                    {"name": "return_date"}
                ]
            },
            {"name": "budget"},
            {"name": "travelers"},
            {"name": "duration"}
        ]


    # Add ML entity to app

    modelId = client.model.add_entity(app_id, versionId, name="order", children=mlEntityDefinition)
   
    # define phraselist - add phrases as significant vocabulary to app


    # Get entity and sub-entities :
    modelObject = client.model.get_entity(app_id, versionId, modelId)

    departure_fromId = get_grandchild_id(modelObject, "location", "departure_location")
    return_fromId = get_grandchild_id(modelObject, "location", "return_location")
    departure_date = get_grandchild_id(modelObject, "date", "departure_date")
    return_dateId = get_grandchild_id(modelObject, "date", "return_date")
    print("Liste des entités :", [child.name for child in modelObject.children])
    budgetId = get_child_id(modelObject, "budget")
    travelersId = get_child_id(modelObject, "travelers")
    durationId = get_child_id(modelObject, "duration")


    # Add model as feature to subentity model
    prebuiltFeatureRequiredDefinition = {"model_name" : "geographyV2", "is_required": True}
    client.features.add_entity_feature(app_id, versionId, departure_fromId, prebuiltFeatureRequiredDefinition)
    client.features.add_entity_feature(app_id, versionId, return_fromId, prebuiltFeatureRequiredDefinition)
    prebuiltFeatureRequiredDefinition = {"model_name": "datetimeV2", "is_required": True}
    client.features.add_entity_feature(app_id, versionId, departure_date, prebuiltFeatureRequiredDefinition)
    client.features.add_entity_feature(app_id, versionId, return_dateId, prebuiltFeatureRequiredDefinition)
    prebuiltFeatureRequiredDefinition = {"model_name": "money", "is_required": True}
    client.features.add_entity_feature(app_id, versionId, budgetId, prebuiltFeatureRequiredDefinition)
    prebuiltFeatureNotRequiredDefinition = {"model_name": "number", "is_required": False}
    client.features.add_entity_feature(app_id, versionId, travelersId, prebuiltFeatureNotRequiredDefinition)
    client.features.add_entity_feature(app_id, versionId, durationId, prebuiltFeatureNotRequiredDefinition)


    # Add phraselist as feature to subentity model
    
    # Add utterances examples to intents ----------------------------------------------

    # Define labeled examples :

    BookFlight_utterance = {
        "text": "Hello. Id'like to book a flight from Paris to New-York, leaving on Saturday, August 13, 2016 and returning on Tuesday, August 16, 2016. I have a budget of $3700. ",
        "intentName": intentNames[0],
        "entityLabels": [
            {
                "startCharIndex": 37,
                "endCharIndex": 159,
                "entityName": "order",
                "children": [
                    {
                        "startCharIndex": 37,
                        "endCharIndex": 53,
                        "entityName": "location",
                        "children": [
                            {
                                "startCharIndex": 37,
                                "endCharIndex": 41,
                                "entityName": "departure_location"
                            },
                            {
                                "startCharIndex": 46,
                                "endCharIndex": 53,
                                "entityName": "return_location"
                            }]
                    },
                    {
                        "startCharIndex": 67,
                        "endCharIndex": 133,
                        "entityName": "date",
                        "children": [
                            {
                                "startCharIndex": 67,
                                "endCharIndex": 91,
                                "entityName": "departure_date"
                            },
                            {
                                "startCharIndex": 110,
                                "endCharIndex": 133,
                                "entityName": "return_date"
                            }]
                        },
                    {
                        "startCharIndex": 155,
                        "endCharIndex": 159,
                        "entityName": "budget"
                        }
                    ]
                }
            ]
        }

    Confirm_utterance = {
        "text": "OK",
        "intentName": intentNames[1]
    }

    Greetings_utterance = {
        "text": "Hello",
        "intentName": intentNames[2]
    }

    # Add an example for the entity
    # Enable nested children to allow using multiple models with the same name
    # The "quantity" subentity and the phraselise could have the same exact name if this is set to True
    client.examples.add(app_id, versionId, BookFlight_utterance, {"enableNestedChildren": True})
    client.examples.add(app_id, versionId, Confirm_utterance, {"enableNestedChildren": False})
    client.examples.add(app_id, versionId, Greetings_utterance, {"enableNestedChildren": False})

    # Train the model ---------------------------------------------------------

    client.train.train_version(app_id, versionId)
    waiting = True
    while waiting:
        info = client.train.get_status(app_id, versionId)

        # get_status returns a list of training statuses , one for each model. Loop through them and make sure all are done.
        waiting = any(map(lambda x: "Queued" == x.details.status or "InProgess" == x.details.status, info))
        if waiting :
            print("Waiting 10 seconds for training to complete")
            time.sleep(10)
        else:
            print("Trained")
            waiting = False
    
    # Publish the app ---------------------------------------------------------

    responseEndpointInfo = client.apps.publish(app_id, versionId, is_staging=False)

    # Authenticate prediction runtime client ----------------------------------

    runtimeCredentials = CognitiveServicesCredentials(authoringKey) # for test only. For production, use prediction key
    clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)

    # Get a prediction from runtime --------------------------------------------

    # Production == slot name
    predictionRequest = {"query": "Hi. i'd like to fly from New-York to Las-Vegas on August 10, 2021"}

    predictionResponse = clientRuntime.prediction.get_slot_prediction(app_id, "Production", predictionRequest)
    print(f"Top intent : {predictionResponse.prediction.top_intent}")
    print(f"Sentiment : {predictionResponse.prediction.sentiment}")

    for intent in predictionResponse.prediction.intents:
        print(f"\t{json.dumps(intent)}")
    print(f"Entities : {predictionResponse.prediction.entities}")




quickstart()