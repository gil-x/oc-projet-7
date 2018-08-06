#! /usr/bin/env python3
# coding: utf-8

import requests

from helpers.config import Config
# from config import Config.API_KEY

class LocationFinder:
    """
    Go ask Google Geocoding API to get address and coordinates.
    The 'find_location' method returns a dictionnary.
    """
    def __init__(self):
        self.api = "https://maps.googleapis.com/maps/api/geocode/json"
        self.API_KEY = Config.API_KEY

    def find_location(self, intent):
        """
        Uses requests libray to ask Google API.
        """

        args = {
            "address": intent,
            "key": self.API_KEY,
        }

        try:
            response = requests.get(self.api, params=args)
            # print(response)
            data = response.json()
            # print(data)

            if data == {'results': [], 'status': 'ZERO_RESULTS'}:
                return { "api_response": "no_result"}
            else:
                return {
                    "address": data["results"][0]["formatted_address"],
                    "latitude": data["results"][0]["geometry"]["location"]["lat"],
                    "longitude": data["results"][0]["geometry"]["location"]["lng"],
                    "api_response": "ok",
                }
            return { "api_response": "unknow_error" }

        except: # TODO Trouver le type d'erreur !
            return { "api_response": "connection_error" }
        



def main():
    location_finder = LocationFinder()
    testing = True

    while testing is True:
        message = input("Type some text to find in Google API or juste <ENTER> to use a prebuilt test sentence.\n")
        if message == "":
            test_sentence = "Mairie du 12e Paris"
            print("Test sentence:")
            print(test_sentence)
            print("Response:")
            print(location_finder.find_location(test_sentence))
        else:
            print(location_finder.find_location(message))
        
        keep_testing = input("Continue testing (Y/N)?\n").lower().strip()
        if keep_testing != "y":
            testing = False

if __name__ == "__main__":
    main()
