#! /usr/bin/env python3
# coding: utf-8

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
        intent = self.parser.get_intent(message)
        response = {}

        # Detect a QUIT intent

        # Detect an HELLO intent and says hello too
        if intent["hello"]:
            response["hello"] = "[hello]"
    
        # Get the location
        location = self.location_finder.find_location(intent["intent"])

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

        return response


def main():
    grandpy = GrandPyBot()
    message = input("What do you want to tell to GrandPy?\n")
    print(grandpy.ask(message))

if __name__ == "__main__":
    main()