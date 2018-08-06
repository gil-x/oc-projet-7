#! /usr/bin/env python3
# coding: utf-8

import random

from helpers.parser import Parser
from helpers.location_finder import LocationFinder
from helpers.story_finder import StoryFinder

class GrandPyBot:
    """
    This class leads.
    The ask method receives a dictionnary like {
            'questions': 'some text', 'intent': 'some text + more text',
            'affirmative': False, 'negative': False, 'hello': False, 'quit': False, 'thanks': False
            }
    The field 'questions' shall not be used in this version of GranPyBot.
    """
    def __init__(self):
        self.parser = Parser()
        self.location_finder = LocationFinder()
        self.story_finder = StoryFinder()
    
    def ask(self, message):
        print("new message incoming")
        intent = self.parser.get_intent(message)
        response = {}

        # Detect a QUIT intent
        if intent["quit"]:
            response["quit"] = random.sample([
                "Au revoir !",
                "Au revoir mon petit.",
                "Bien le bonjour !",
                "Adieu.",
                "Bon bin au revoir.",
                "Bon bin adieu.",
                ], 1)[0]

        # Detect an HELLO intent and says hello too
        if intent["hello"]:
            response["hello"] = random.sample([
                "Bonjour !",
                "Bonjour mon petit.",
                "À bientôt mon petit.",
                "Hum...? Oh, salut.",
                "Zzzz.. Oh ! Bonjour !",
                ], 1)[0]
    
        # Get the location
        location = self.location_finder.find_location(intent["intent"])
        print("location:", location)

        # Simulate Grandpy reflexion
        response["reflexion"] = random.sample([
                "Ah oui, je me souviens...",
                "Mmmm... Laisse-moi deux minutes...",
                "Mais bien sûr que je connais !",
                "Ahhhh, j'ai vécu dix dans dans ce coin.",
                "Bien sûr, bien sûr !",
                ], 1)[0]
        
        # Simulate Grandpy reflexion
        response["localize"] = random.sample([
                "C'est là :",
                "C'est à peu près là :",
                "D'après mon cerveau-API, c'est à peu près là :",
                "Mon Google sense me dit que c'est par là :",
                "Si ma mémoire est bonne c'est là :",
                "Si ma mémoire est bonne - et elle est aussi fiable qu'une API Google ! - c'est là :",
                ], 1)[0]


        if location["api_response"] == "ok":
            # print("address:", location["address"])
            # print("coordinates:", location["latitude"], location["longitude"])
            response["location"] = {
                "address": location["address"],
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                }
        else:
            # print("[No location found]")
            response["location"] = { "[No location found]" }

        # Get some places stories
        places_stories = self.story_finder.get_story(location["latitude"], location["longitude"])
        places_stories_textual_list = []
        if len(places_stories) > 1:
            for place in places_stories:
                # print(place)
                places_stories_textual_list.append({
                    "name": place["name"],
                    "extract": place["extract"],
                })
            response["stories"] = places_stories_textual_list
        else:
            print("[No story found]")
            response["stories"] = "[No story found]"

        # Show the map
        if response["location"] != { "[No location found]" }:
            response["map"] = {
                "text": "[Look at the map]",
                "latitude": location["latitude"],
                "longitude": location["longitude"],
            }

        # After story
            response["end"] = "[FINI]"


        # API key
            # response["apikey"] = 

        return response