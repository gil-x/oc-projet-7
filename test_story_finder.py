#! /usr/bin/env python3
# coding: utf-8

import requests
import unittest
import json

from unittest.mock import patch
from helpers.story_finder import StoryFinder

class TestStoryFinder(unittest.TestCase):
    """
    Emulate the API response in case of success and failure.
    """
    story_finder = StoryFinder()

    @patch('helpers.story_finder.requests.get')
    def test_find_a_story(self, monkeypatch):

        # latitude|longitude arg:
        arg = {'latitude': 48.8558986, 'longitude': 2.298087500000065}

        # Mock json API response:
        api_response = { 'batchcomplete': '', 'query': { 'pages': { '104136': {
            'extract': 'Le Champ-de-Mars est ' 'un vaste jardin ' 'public, entièrement '
            'ouvert et situé à ' 'Paris dans le 7e ' 'arrondissement, entre ' 'la tour Eiffel au '
            "nord-ouest et l'École " 'militaire au sud-est. ' 'Avec ses 24,5 ha, le '
            'jardin du Champ de ' "Mars est l'un des plus " 'grands espaces verts '
            "de Paris. Riche d'une " 'histoire bicentenaire, ' 'le Champ-de-Mars '
            'accueille les ' 'Parisiens et les ' 'touristes toute ' "l'année autour d'un "
            'vaste ensemble ' "d'activités.", 'index': 0, 'ns': 0, 'pageid': 104136,
            'title': 'Champ-de-Mars (Paris)'},
            '1127447': { 'extract': "L'Exposition " 'universelle de 1900 ' "ou L'Exposition de "
            'Paris 1900 est la ' 'cinquième exposition ' 'universelle organisée '
            'à Paris après celle ' 'de 1855, celle de ' '1867, celle de 1878 ' 'et celle de 1889. \n'
            'Annoncée le 13 ' 'juillet 1892, elle ' 'est inaugurée le 14 ' 'avril 1900 par le '
            'président Émile ' "Loubet et s'ouvre au " 'public le 15 avril. ' 'Elle se termine le 12 '
            'novembre, après 212 ' "jours d'ouverture. " 'Elle accueille plus ' 'de 48 millions de '
            'visiteurs.\n' 'Manifestation ' 'emblématique de la ' 'Belle Époque et de '
            "l'Art nouveau, elle " 'lègue à Paris ' 'plusieurs bâtiments ' 'dont le Petit Palais '
            'et le Grand Palais. ' 'Le thème est « Bilan ' 'd’un siècle ». Par ' 'ailleurs, les IIe '
            'Jeux olympiques de ' "l'ère moderne se " 'déroulent à Paris ' 'dans le cadre de '
            'cette exposition ''universelle.', 'index': 1, 'ns': 0, 'pageid': 1127447,
            'title': 'Exposition universelle ' 'de 1900'},
            '1159506': {   'extract': "L'Exposition " 'universelle de 1867, ' 'également appelée '
            'Exposition ' "universelle d'art et " "d'industrie, est " 'chronologiquement la '
            'septième Exposition ' 'universelle et la ' 'seconde se déroulant '
            'à Paris après celle ' "de 1855. Elle s'est " 'tenue du 1er avril au '
            '3 novembre 1867 sur ' 'le Champ-de-Mars, à ' 'Paris. 41 pays ' 'étaient représentés à '
            "l'Exposition.", 'index': 2, 'ns': 0, 'pageid': 1159506,
            'title': 'Exposition universelle ' 'de 1867'},
            '1226355': { 'extract': 'L’allée ' 'Adrienne-Lecouvreur ' 'est une rue du 7e '
            'arrondissement de ' 'Paris.', 'index': 3, 'ns': 0, 'pageid': 1226355,
            'title': 'Allée ' 'Adrienne-Lecouvreur'},
            '1852424': { 'extract': 'Le théâtre guignol du ' 'Champ de Mars a été '
            'fondé[Quand ?] par ' 'Luigi Tirelli et ' 'Gilbert Chalvet à ' "l'intérieur des "
            'jardins du Champ de ' 'Mars, côté 7e ' "arrondissement. C'est " 'une salle de théâtre '
            'spécialement dédiée ' 'aux marionnettes à ' 'gaine et plus ' 'particulièrement à '
            'Guignol. Le bâtiment ' 'et la salle sont ' "chauffés l'hiver et " "climatisés l'été. Il "
            "s'agit d'un des plus " 'grands théâtres de ' 'marionnettes de Paris ' "puisqu'il contient "
            'plus de 200 places,.\n' 'Une représentation ' 'dure environ 45 ' 'minutes. Leur '
            'répertoire compte une ' 'trentaine de pièces ' 'comme Le Trésor du ' 'roi Dagobert, Guignol '
            'au Mexique, La Belle ' 'au bois dormant, ' 'Blanche-Neige et les ' 'Sept Nains, Les '
            'Aventures du prince ' 'Carabi, Les Graines ' 'magiques, Le trésor ' 'de la sultane, etc.\n'
            'Les spectacles sont ' 'toujours adaptés de ' 'façon que Guignol ' 'soit présent dans '
            'chaque histoire.\n' 'Avec environ 600 ' 'marionnettes et 200 ' 'décors ou éléments de '
            "décors, c'est l'une " 'des plus grandes ' 'collections ' 'parisiennes.[réf. '
            'nécessaire]', 'index': 4, 'ns': 0, 'pageid': 1852424,
            'title': 'Théâtre guignol du ' 'Champ de Mars'},
            '2889421': { 'extract': "L'avenue " 'Anatole-France est ' 'une allée du ' 'Champ-de-Mars dans le '
            '7e arrondissement de ' 'Paris.', 'index': 5, 'ns': 0, 'pageid': 2889421,
            'title': 'Avenue Anatole-France ' '(Paris)'},
            '2889422': { 'extract': "L'avenue Pierre-Loti " 'est une allée du ' 'Champ de Mars dans le '
            '7e arrondissement de ' 'Paris.', 'index': 6, 'ns': 0, 'pageid': 2889422,
            'title': 'Avenue Pierre-Loti'},
            '2889454': {   'extract': "L'avenue " 'Joseph-Bouvard est ' 'une voie située dans '
            'le quartier du ' 'Gros-Caillou du 7e ' 'arrondissement de ' 'Paris.',
            'index': 7, 'ns': 0, 'pageid': 2889454,
            'title': 'Avenue Joseph-Bouvard'},
            '5422116': { 'extract': "L'avenue du " 'Général-Marguerite ' 'est une voie du 7e '
            'arrondissement de ' 'Paris, en France.', 'index': 8, 'ns': 0, 'pageid': 5422116,
            'title': 'Avenue du ' 'Général-Marguerite'},
            '6957361': { 'extract': 'La place ' 'Jacques-Rueff est une ' 'voie située dans le '
            'quartier du ' 'Gros-Caillou du 7e ' 'arrondissement de ' 'Paris.',
            'index': 9, 'ns': 0, 'pageid': 6957361,
            'title': 'Place Jacques-Rueff'
        }}}}
        
        # Expected result:
        result = [
            { 'extract':
                'Le Champ-de-Mars est un vaste jardin public, entièrement '
                'ouvert et situé à Paris dans le 7e arrondissement, entre '
                "la tour Eiffel au nord-ouest et l'École militaire au "
                'sud-est. Avec ses 24,5 ha, le jardin du Champ de Mars est '
                "l'un des plus grands espaces verts de Paris. Riche d'une "
                'histoire bicentenaire, le Champ-de-Mars accueille les '
                "Parisiens et les touristes toute l'année autour d'un vaste "
                "ensemble d'activités.",
                'name': 'Champ-de-Mars (Paris)'},
            { 'extract':
                "L'Exposition universelle de 1900 ou L'Exposition de Paris "
                '1900 est la cinquième exposition universelle organisée à '
                'Paris après celle de 1855, celle de 1867, celle de 1878 et '
                'celle de 1889. \n'
                'Annoncée le 13 juillet 1892, elle est inaugurée le 14 '
                "avril 1900 par le président Émile Loubet et s'ouvre au "
                'public le 15 avril. Elle se termine le 12 novembre, après '
                "212 jours d'ouverture. Elle accueille plus de 48 millions "
                'de visiteurs.\n'
                "Manifestation emblématique de la Belle Époque et de l'Art "
                'nouveau, elle lègue à Paris plusieurs bâtiments dont le '
                'Petit Palais et le Grand Palais. Le thème est « Bilan d’un '
                "siècle ». Par ailleurs, les IIe Jeux olympiques de l'ère "
                'moderne se déroulent à Paris dans le cadre de cette '
                'exposition universelle.',
                'name': 'Exposition universelle de 1900'},
            { 'extract':
                "L'Exposition universelle de 1867, également appelée "
                "Exposition universelle d'art et d'industrie, est "
                'chronologiquement la septième Exposition universelle et la '
                'seconde se déroulant à Paris après celle de 1855. Elle '
                "s'est tenue du 1er avril au 3 novembre 1867 sur le "
                'Champ-de-Mars, à Paris. 41 pays étaient représentés à '
                "l'Exposition.",
                'name': 'Exposition universelle de 1867'},
            { 'extract':
                'L’allée Adrienne-Lecouvreur est une rue du 7e '
                'arrondissement de Paris.',
                'name': 'Allée Adrienne-Lecouvreur'},
            { 'extract':
                'Le théâtre guignol du Champ de Mars a été fondé[Quand ?] '
                "par Luigi Tirelli et Gilbert Chalvet à l'intérieur des "
                "jardins du Champ de Mars, côté 7e arrondissement. C'est "
                'une salle de théâtre spécialement dédiée aux marionnettes '
                'à gaine et plus particulièrement à Guignol. Le bâtiment et '
                "la salle sont chauffés l'hiver et climatisés l'été. Il "
                "s'agit d'un des plus grands théâtres de marionnettes de "
                "Paris puisqu'il contient plus de 200 places,.\n"
                'Une représentation dure environ 45 minutes. Leur '
                'répertoire compte une trentaine de pièces comme Le Trésor '
                'du roi Dagobert, Guignol au Mexique, La Belle au bois '
                'dormant, Blanche-Neige et les Sept Nains, Les Aventures du '
                'prince Carabi, Les Graines magiques, Le trésor de la '
                'sultane, etc.\n'
                'Les spectacles sont toujours adaptés de façon que Guignol '
                'soit présent dans chaque histoire.\n'
                'Avec environ 600 marionnettes et 200 décors ou éléments de '
                "décors, c'est l'une des plus grandes collections "
                'parisiennes.',
                'name': 'Théâtre guignol du Champ de Mars'},
            {'extract':
                "L'avenue Anatole-France est une allée du Champ-de-Mars "
                'dans le 7e arrondissement de Paris.',
                'name': 'Avenue Anatole-France (Paris)'},
            { 'extract':
                "L'avenue Pierre-Loti est une allée du Champ de Mars dans "
                'le 7e arrondissement de Paris.',
                'name': 'Avenue Pierre-Loti'},
            { 'extract': "L'avenue Joseph-Bouvard est une voie située dans le "
                'quartier du Gros-Caillou du 7e arrondissement de Paris.',
                'name': 'Avenue Joseph-Bouvard'},
            { 'extract': "L'avenue du Général-Marguerite est une voie du 7e "
                'arrondissement de Paris, en France.',
                'name': 'Avenue du Général-Marguerite'},
            { 'extract': 'La place Jacques-Rueff est une voie située dans le '
                'quartier du Gros-Caillou du 7e arrondissement de Paris.',
                'name': 'Place Jacques-Rueff'}
            ]

        monkeypatch.return_value.json.return_value = api_response

        assert self.story_finder.get_story(arg["latitude"], arg["longitude"]) == result



    @patch('helpers.story_finder.requests.get')
    def test_dont_find_a_story(self, monkeypatch):

        # latitude|longitude arg:
        arg = {'latitude': 999, 'longitude': 999}

        # Mock json API response:
        api_response = { 'error':
                {
                    '*': 'See https://fr.wikipedia.org/w/api.php for API usage. '
                'Subscribe to the mediawiki-api-announce mailing list at '
                '&lt;https://lists.wikimedia.org/mailman/listinfo/mediawiki-api-announce&gt; '
                'for notice of API deprecations and breaking changes.',
                'code': 'invalid-coord',
                'info': 'Invalid coordinate provided'
                },
                'servedby': 'mw1284'
            }
        
        # Expected result:
        result = [{ "api_response": "no_result" }]

        monkeypatch.return_value.json.return_value = api_response

        assert self.story_finder.get_story(arg["latitude"], arg["longitude"]) == result