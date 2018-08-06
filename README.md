# GrandPyBot

Web application running on Flask (Python web Framework), created for the *project 7* of the course _"Développeur d'application Python"_ of french school *Openclassroom*.


## Features
_GrandPy_ is a tiny chatbot.
The website is a simple web page displaying a chat.
User just types a message to ask if _GrandPy_ knows a place. He will try to find an exact address.
If your message is too verbose, _GrandPy_ may find suprising results!


## Tech

### Procedure

1. User send a message. This one is AJAX handled.
2. The application parses the message, trying to leave behing all non significant words.
3. The application uses the parsed message to ask Google Maps API to get a precise location, wich give address, latitude, longitude.
4. The application uses the loaction to ask Mediawiki API and get some extra information about a place near the location.
5. The website displays the found informations and a minimap in the chat. If nothing is found, or if some error occurs, GrandPy says also something.

### Specs

* There is no database nor cookies: *nothing* is saved when the session get close.
* The application provide *unit tests*, written for pytest.
* The application can run in a simplier way, as a Python script, by running *console_grandpy.py*, just be sure to match the requirements.


## Licence
All code and the incredible graphic work is free. You can redistribute it and/or modify it under the terms of the Do What The Fuck You Want To Public License, Version 2, as published by Sam Hocevar. See [wtfpl](http://www.wtfpl.net/) for more details.