import os, os.path

import cherrypy

from governmentParser import GenerateArrays

import random


""" lans for the future: 
1. Declutter Code
2. Add support for statistics 
3. Deal with "array out of bounds" bug 
 """
class PageGenerator:

    # generates the needed arrays and stores them locally
    priceArray = GenerateArrays()[0]
    taskArray = GenerateArrays()[1]
    urlArray = GenerateArrays()[2]


    def GenerateGameParameters(priceArray):
        # Generate Random button to be the correct one
        CorrectAnswerButton = random.randint(0, 2)

        # generates Random Index for Guessing since the data is inconsistent we take the min length of 3 arrays and get the MaxIndex = 50
        GameIndex = random.randint(0, 50)

        return CorrectAnswerButton, GameIndex

    def ButtonAssignment(CorrectAnswerButton, GameIndex, priceArray):
        Button0 = ""
        Button1 = ""
        Button2 = ""
        #To maximise randomisation we create 2 functions - CoefficentGenerator and Multiplyer
        def CoefficentGenerator():
            return random.randint(1, 1000000)

        def Multiplyer():
            array = [-1, 1]

            return array[random.randint(0, 1)]

        if CorrectAnswerButton == 0:
            Button0 = str(priceArray[GameIndex])
            Button1 = str(abs(priceArray[GameIndex] + Multiplyer() * CoefficentGenerator()))
            Button2 = str(abs(priceArray[GameIndex] + Multiplyer() * CoefficentGenerator()))

        if CorrectAnswerButton == 1:
            Button0 = str(abs(priceArray[GameIndex] + Multiplyer() * CoefficentGenerator()))
            Button1 = str(priceArray[GameIndex])
            Button2 = str(abs(priceArray[GameIndex] + Multiplyer() * CoefficentGenerator()))


        if CorrectAnswerButton == 2:
            Button0 = str(abs(priceArray[GameIndex] + Multiplyer() * CoefficentGenerator()))
            Button1 = str(abs(priceArray[GameIndex] + Multiplyer() * CoefficentGenerator()))
            Button2 = str(priceArray[GameIndex])

        global answer
        answer = CorrectAnswerButton


        return Button0, Button1, Button2, GameIndex, CorrectAnswerButton



    #Everything that has to do with webpage handeling

    test = ButtonAssignment(GenerateGameParameters(priceArray)[0], GenerateGameParameters(priceArray)[1], priceArray)

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('HTML.html').read().format(PageGenerator.taskArray[PageGenerator.test[3]], PageGenerator.urlArray[PageGenerator.test[3]], PageGenerator.test[0], PageGenerator.test[1], PageGenerator.test[2])


@cherrypy.expose
class StringGeneratorWebService(object):
    answer = 3



    @cherrypy.tools.accept(media='text/plain')

    #PLAYAGAIN is decontructed and buit into a string array with | seperators because JS reads it as a string
    def PLAYAGAIN(self):
        test = PageGenerator.ButtonAssignment(PageGenerator.GenerateGameParameters(PageGenerator.priceArray)[0], PageGenerator.GenerateGameParameters(PageGenerator.priceArray)[1],PageGenerator.priceArray)

        NewTask = str("|"+PageGenerator.taskArray[test[3]]+"|")

        NewUrl = str(PageGenerator.urlArray[test[3]]+"|")

        Button0 = str(test[0] + "|")

        Button1 = str(test[1] + "|")

        Button2 = str(test[2] + "|")

        global answer

        answer = test[4]


        NewGame = [NewTask, NewUrl, Button0, Button1, Button2]
        print(NewGame)

        return NewGame


    def BUTTON0(self):
        global answer
        if answer == 0:
            return "Correct"
        else:
            return "Wrong"




    def BUTTON1(self):
        global answer
        if answer == 1:
            return "Correct"
        else:
            return "Wrong"

    def BUTTON2(self):
        global answer
        if answer == 2:
            return "Correct"
        else:
            return "Wrong"

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = StringGenerator()
    webapp.generator = StringGeneratorWebService()
    cherrypy.quickstart(webapp, '/', conf)








