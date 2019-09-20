from kivy.app import App
# kivy.require("1.0.9")
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.core.audio import SoundLoader

import psutil
import requests
import speech_recognition as sr
import time


class ScreenManagement(ScreenManager):
    pass


class MainScreen(Screen):
    pass


class ScoreScreen(Screen):
    pass


class ImageViewer(GridLayout):
    path = "./images/"
    image_title = "kid"
    images = ["kid", "kid2"]

    def __init__(self, **kwargs):
        super(ImageViewer, self).__init__(**kwargs)

    def loadImage(self, name):
        image = self.path + str(name) + '.jpeg'
        return image


class GameController(GridLayout):
    name = "ghassen"
    result_id = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameController, self).__init__(**kwargs)

    def playSound(self, name):
        path = "./sounds/"
        fname = path + str(name)+".wav"
        sound = SoundLoader.load(fname)
        if sound is not None:
            sound.volume = 0.5
            sound.play()

    def listen(self):
        r = sr.Recognizer()
        command = ""
        with sr.Microphone() as source:
            print('Ready...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

        try:
            command = r.recognize_google(audio, language="en-US",)
            print('You said: ' + command + '\n')

        # loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            print('Retry')

        return command


class GameProgress(BoxLayout):
    def __init__(self, **kwargs):
        super(GameProgress, self).__init__(**kwargs)
    wrongAnsewrs = 0
    total = 20

    def repeat():
        self.wrongAnsewrs += 1

    def getScore(self):
        return (self.wrongAnsewrs/self.total)*100


class GameScreen(Screen):
    i = 0
    imageViewer = ImageViewer()
    gameController = GameController()
    gameProgress = GameProgress()
    titles = ["alien", "elephant", "kid"]
    source = imageViewer.loadImage(titles[0])
    imageTitle = titles[0]

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        command = ""
        image = self.imageViewer.loadImage(self.titles[self.i])

        # initialisation

    def getImage(self):
        return self.imageViewer.loadImage(self.titles[self.i])

    def play(self):
        self.gameController.playSound(self.titles[self.i])

    def listenToMe(self):
        # labels
        resultLabel = self.ids['result_label']
        image = self.ids['image_id']
        imageLabel = self.ids['image_label']
        resultLabel.text = "*   *   *"
        resultLabel.color = [0, 0, 0, 1]

        command = self.gameController.listen()

        resultLabel.text = command
        if(self.titles[self.i] == str(command) and self.i < len(self.titles)):

            resultLabel.text = "*   *   *"
            resultLabel.color = [0, 1, 0, 1]
            time.sleep(0.5)
            self.i += 1
            image.source = self.imageViewer.loadImage(self.titles[self.i])
            imageLabel.text = self.titles[self.i]

        else:
            resultLabel.color = [1, 0, 0, 1]
            self.gameProgress.wrongAnsewrs += 1
            print("different")


game = Builder.load_file("game.kv")


class Game(App):

    def build(self):
        return game


if __name__ == '__main__':
    Game().run()
