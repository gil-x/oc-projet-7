#! /usr/bin/env python3
# coding: utf-8

import requests
import pprint

pp = pprint.PrettyPrinter(indent=4)

class StoryFinder:
    """
    Go ask Wikimedia API for some informations around a location.
    The 'get_story' method returns a dictionnary.
    """
    def __init__(self):
        self.api = "https://fr.wikipedia.org/w/api.php"

    def get_story(self, latitude, longitude):
        args = {
            "action": "query",
            "generator" : "geosearch",
            "ggsradius": 10000,
            "ggscoord": str(latitude) + "|" + str(longitude),
            "prop": "extracts",
            "exintro" : "",
            "explaintext" : "",
            "format": "json", 
        }

        try:
            response = requests.get(self.api, params=args)
            data = response.json()
            stories_list = []

            try:
                if data["error"]:
                    return [{ "api_response": "no_result"}]
            except KeyError:
                pass
            
            for page in data["query"]["pages"]:
                name = data["query"]["pages"][page]["title"]
                extract = data["query"]["pages"][page]["extract"]
                if len(extract) > 10:
                    stories_list.append({
                        "name": name,
                        "extract": extract.replace("[réf. nécessaire]", ""),
                    })
            return stories_list

        except: # TODO Trouver le type d'erreur !
            return [{ "api_response": "connection_error" }]


def main():
    import random # QUESTION : on a le droit de faire ça ?

    story_finder = StoryFinder()
    testing = True

    test_coordinates_set = [
        { "latitude" : 999, "longitude" : 999, },
        { "latitude" : 48.8558986, "longitude" : 2.298087500000065, },
        { "latitude" : 38.9071923, "longitude" : -77.03687070000001, },
        { "latitude" : -0.228021, "longitude" : 15.82765900000004, },
        { "latitude" : 35.6894875, "longitude" : 139.69170639999993, },
        { "latitude" : 55.9692178, "longitude" : 12.54233679999993, },
    ]
    test_coordinates = random.sample(test_coordinates_set, 1)[0]
    print("=================")
    print("Test coordinates:")
    print(test_coordinates)
    print("=================")
    print("Response:")
    pp.pprint(story_finder.get_story(test_coordinates["latitude"], test_coordinates["longitude"]))
    print("===end reponse===")


if __name__ == "__main__":
    main()
