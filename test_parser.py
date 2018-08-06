#! /usr/bin/env python3
# coding: utf-8

from helpers.parser import Parser
# from parser import Parser

class TestParser:
    """
    DOCSTRING
    """
    parser = Parser()

    def test_parse_simple_exclamation(self):
        self.parser.purge()
        message = "Salut le vieux !!!"
        assert self.parser.get_intent(message) == {
            'questions': '',
            'intent': 'vieux',
            'affirmative': False,
            'negative': False,
            'hello': True,
            'quit': False,
            'thanks': False
            }

    def test_parse_question_and_no_end_dot(self):
        self.parser.purge()
        message = "C'est quoi le problème ??? Moi je vois pas"
        assert self.parser.get_intent(message) == {
            'questions': "c'est quoi le problème ?",
            'intent': 'problème vois',
            'affirmative': False,
            'negative': False,
            'hello': False,
            'quit': False,
            'thanks': False
            }

    def test_multi(self):
        self.parser.purge()
        message = "Salut le vieux ! On m'a dit que c'était cool de discuter avec toi... J'espère que c'est vrai, sinon je me tire !!! Qu'est-ce que tu penses de ça mon petit chatbot adoré ?.. Ça te la coupe hein ? Bon, allez ! J'ai plein de questions à te poser ! GO"
        assert self.parser.get_intent(message) == {
            'questions': "qu'est-ce que tu penses de ça mon petit chatbot adoré ? ça te la coupe hein ?", 'intent': "qu'est-ce penses petit chatbot adoré coupe m'a c'était cool discuter go vieux j'espère vrai tire bon allez j'ai questions poser",
            'affirmative': False,
            'negative': False,
            'hello': True,
            'quit': False,
            'thanks': False
            }

    def test_empty_message(self):
        parser = Parser()
        self.parser.purge()
        message = ""
        assert self.parser.get_intent(message) == {
            'questions': "",
            'intent': "",
            'affirmative': False,
            'negative': False,
            'hello': False,
            'quit': False,
            'thanks': False
            }