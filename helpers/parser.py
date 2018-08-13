#! /usr/bin/env python3
# coding: utf-8

from helpers.config import *
# from config import *


class Parser:
    """
    Analyse user messages and filter useful words and sentences.
    """
    def __init__(self):
        self.affirmative_words = AFFIRMATIVE_WORDS
        self.negative_words = NEGATIVE_WORDS
        self.hello_words = HELLO_WORDS
        self.quit_words = QUIT_WORDS
        self.thanks_words = THANKS_WORDS
        self.stop_words = STOP_WORDS
        self.exclamations = []
        self.sentences = []
        self.questions = []
        self.affirmative = False
        self.negative = False
        self.hello = False
        self.quit = False
        self.thanks = False
        self.intent = []

    def get_intent(self, message):
        """
        Clean message from punctuation, useless whitespaces and generics words.
        Gets intents by comparing each usefull word to lists of target words.
        Returns a dictionnary with the cleaned message and intents as booleans.
        
        """
        message = message.lower() + "."
        message = message.replace("..", ".").replace("...", ".").replace("..", ".")
        message = message.replace("!!!", "!").replace("!!", "!")
        message = message.replace("?...", "?").replace("?..", "?").replace("?.", "?").replace("??", "?").replace("???", "?").replace("??", "?")
        # Now the punctuation should be perfect!

        while len(message) > 1:
            # Looks for punctuation, register indexes,
            # then uses indexes to cut in sentences.
            # Message will be shortened until all sentences are found
            # and then registered according to the ending punctuation
            sentence_stops = [message.find("."), message.find("!"), message.find("?")]
            sentence_stops = list(filter(lambda i: i != -1, sentence_stops))
            sentence_stops.sort()
            sentence = message[:sentence_stops[0]] + message[sentence_stops[0]]
            sentence_type = message[sentence_stops[0]]
            if sentence_type == "?":
                self.questions.append(sentence.strip())
            elif sentence_type == "!":
                self.exclamations.append(sentence.strip())
            else:
                self.sentences.append(sentence.strip())
            message = message[(sentence_stops[0] + 1):]

        for sentence_group in [self.questions, self.sentences, self.exclamations]:
            # Looks in all sentences to remove stop-words
            # get the purpose of the sentence ...
            # ... and the intent should be the remaining significant words
            for sentence in sentence_group:
                for word in sentence.split():
                    word = word.replace(".", "").replace("!", "").replace("?", "").replace(",", "")
                    if word in self.affirmative_words:
                        self.affirmative = True
                    if word in self.negative_words:
                        self.negative = True
                    if word in self.hello_words:
                        self.hello = True
                    if word in self.quit_words:
                        self.quit = True
                    if word in self.thanks_words:
                        self.thanks = True
                    if word not in self.stop_words:
                        self.intent.append(word)

        parsed_response = {
            "questions" : " ".join(self.questions).replace("  ", " ").strip(),
            "intent": " ".join(self.intent).replace("  ", " ").strip(),
            "affirmative": self.affirmative,
            "negative": self.negative,
            "hello": self.hello,
            "quit": self.quit,
            "thanks": self.thanks,
        }

        print(parsed_response)

        self.purge()

        return(parsed_response)

    def purge(self):
        """
        Purge all attributes.
        """
        self.exclamations = []
        self.sentences = []
        self.questions = []
        self.affirmative = False
        self.negative = False
        self.hello = False
        self.quit = False
        self.thanks = False
        self.intent = []


def main():
    parser = Parser()
    testing = True

    while testing is True:
        message = input("""
Type some text to parse or juste <ENTER> to use a prebuilt test sentence.\n""")
        if message == "":
            test_sentence = """
Salut le vieux ! On m'a dit que c'était cool de
discuter avec toi... J'espère que c'est vrai, sinon je me tire !!!
Qu'est-ce que tu penses de ça mon petit chatbot adoré ?..
Ça te la coupe hein ? Bon, allez ! J'ai plein de questions à te poser ! GO"""
            print("Test sentence:")
            print(test_sentence)
            print("Response:")
            print(parser.get_intent(test_sentence))
        else:
            print(parser.get_intent(message))
        keep_testing = input("Continue testing (Y/N)?\n").lower().strip()
        if keep_testing != "y":
            testing = False

if __name__ == "__main__":
    main()
