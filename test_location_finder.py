#! /usr/bin/env python3
# coding: utf-8

import requests
import unittest
import json
from io import BytesIO

from unittest.mock import patch
from helpers.config import Config
# from config import API_KEY
from helpers.location_finder import LocationFinder
# from location_finder import LocationFinder

class TestLocationFinder(unittest.TestCase):
    """
    Emulate the API response in case of success and failure.
    """
    location_finder = LocationFinder()

    @patch('helpers.location_finder.requests.get')
    def test_find_a_location(self, monkeypatch):

        # The intent :
        arg = "Mairie du 12e Paris"

        # Mock json API response:
        api_response = {'results':
            [{'address_components':
                [
                    {'long_name': '130', 'short_name': '130',
                        'types': ['street_number']},
                    {'long_name': 'Avenue Daumesnil', 'short_name': 'Avenue Daumesnil',
                        'types': ['route']}, {'long_name': 'Paris', 'short_name': 'Paris',
                        'types': ['locality', 'political']}, {'long_name': 'Paris', 'short_name': 'Paris',
                        'types': ['administrative_area_level_2', 'political']},
                    {'long_name': 'Île-de-France', 'short_name': 'Île-de-France',
                        'types': ['administrative_area_level_1', 'political']},
                    {'long_name': 'France', 'short_name': 'FR',
                        'types': ['country', 'political']},
                    {'long_name': '75012', 'short_name': '75012',
                        'types': ['postal_code']}],
                        'formatted_address': '130 Avenue Daumesnil, 75012 Paris, France', 'geometry': {'location': {'lat': 48.8409134, 'lng': 2.3880995},
                        'location_type': 'ROOFTOP',
                        'viewport': {'northeast': {'lat': 48.84226238029149, 'lng': 2.389448480291502}, 'southwest': {'lat': 48.83956441970849, 'lng': 2.386750519708498}}},
                        'place_id': 'ChIJxQa2sg9y5kcRjB-4yh-d_WM',
                        'types': ['city_hall', 'establishment', 'local_government_office', 'point_of_interest']
                }], 'status': 'OK'}

        # Expected result:
        result = {
            "address" : "130 Avenue Daumesnil, 75012 Paris, France",
            "latitude" : 48.8409134,
            "longitude" : 2.3880995,
            "api_response": "ok",
        }

        monkeypatch.return_value.json.return_value = api_response
        assert self.location_finder.find_location(arg) == result

    @patch('helpers.location_finder.requests.get')
    def test_dont_find_location(self, monkeypatch):

        # The intent:
        arg = "xxxxxxxxxx"

        # Mock json API response:
        api_response = {'results': [], 'status': 'ZERO_RESULTS'}

        # Expected result:
        result = {
            "api_response": "no_result",
        }

        monkeypatch.return_value.json.return_value = api_response
        assert self.location_finder.find_location(arg) == result


