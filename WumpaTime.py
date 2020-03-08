from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.behaviors import FocusBehavior
from kivy.lang import Builder
from kivy_deps import sdl2, glew
import datetime
import time

mainTime = datetime.timedelta(minutes=30, seconds=00, milliseconds=00)
endTime = datetime.timedelta(minutes=00, seconds=00, milliseconds=00)
inputTimes = []
Builder.load_file('WumpaTime.kv')
Window.fullscreen = 'auto'


class WumpaTime(App):
    def build(self):
        layout = FloatLayout()
        layout2 = BoxLayout(orientation='vertical')
        TitleBox = BoxLayout(orientation='vertical')
        box = BoxLayout(spacing=1)
        box2 = BoxLayout()
        bg = Image(source='tlo3.png', allow_stretch=True, keep_ratio=False)
        Tbg = Image(source='Title.png', allow_stretch=False, keep_ratio=True)
        Window.softinput_mode = 'below_target'

        title = Label(size_hint=(None, 0), pos=(0, 0))

        self.lista = Label(text='time left: ' +
                           str(mainTime)[2:10].replace('.', ':'),
                           font_size='100dp', font_name='ComicsCarToon.ttf',
                           outline_color=[0, 0, 0], outline_width=2)

        self.t = TextInput(font_size=200, size_hint_y=None,
                           height=200, halign='right',
                           input_filter='int', multiline=False,
                           background_color=[1, 1, 1, 0],
                           foreground_color=[1, 1, 1, 1],
                           font_name='ComicsCarToon.ttf',
                           hint_text='--:--:--',
                           hint_text_color=[56, 64, 201, 1])

        self.badd = Button(size_hint=(None, None), size=(200, 200),
                           on_release=self.update_label,
                           background_normal='Add1.png',
                           background_down='Add2.png')

        breset = Button(size_hint=(None, None), size=(200, 200),
                        on_release=self.reset_button,
                        background_normal='Reset1.png',
                        background_down='Reset2.png')

        bremove = Button(pos=(0, 200), size_hint=(None, None),
                         size=(200, 200), on_release=self.rem_last,
                         background_normal='Remove1.png',
                         background_down='Remove2.png')

        layout.add_widget(bg)
        TitleBox.add_widget(title)
        TitleBox.add_widget(Tbg)
        layout.add_widget(bremove)
        box.add_widget(breset)
        box.add_widget(self.t)
        box.add_widget(self.badd)
        layout2.add_widget(TitleBox)
        layout2.add_widget(self.lista)
        layout2.add_widget(box)
        layout.add_widget(layout2)

        return layout

    def update_label(self, button_instance):
        global mainTime, inputTimes

        try:
            uinput = str(self.t.text)

            if len(uinput) == 0:
                self.lista.text = 'time left: '
                + str(mainTime)[2:10].replace('.', ':')
            elif len(uinput) < 6:
                uinput = '0' * (6 - len(uinput)) + uinput

            minutes = int(uinput[:2])
            seconds = int(uinput[2:4])
            milliseconds = int(uinput[4:6])*10
            inputTimes.append([uinput[:6]])
            czas = datetime.timedelta(minutes=minutes,
                                      seconds=seconds,
                                      milliseconds=milliseconds)
            odejmowanie = mainTime - czas
            mainTime = odejmowanie
            self.lista.text = 'time left: ' + str(mainTime)[2:10].replace('.', ':')
            self.t.text = ''

            if mainTime <= endTime:
                self.lista.text = "that's it for today!"

        except ValueError:
            self.lista.text = 'time left: ' + str(mainTime)[2:10].replace('.', ':')
            if mainTime <= endTime:
                self.lista.text = "that's it for today!"
            else:
                self.lista.text = 'add some numbers first'
        except TypeError:
            self.lista.text = 'time left: ' + str(mainTime)[2:10].replace('.', ':')
        except SyntaxError:
            self.lista.text = 'time left: ' + str(mainTime)[2:10].replace('.', ':')
        except IndexError:
            self.lista.text = 'time left: ' + str(mainTime)[2:10].replace('.', ':')

    def reset_button(self, button_instance):
        global mainTime, inputTimes
        mainTime = datetime.timedelta(minutes=30, seconds=00, milliseconds=00)
        self.lista.text = 'time left: ' + str(mainTime)[2:10].replace('.', ':')
        self.t.text = ''
        inputTimes = []

    def rem_last(self, button_instance):
        global mainTime, inputTimes
        try:
            timerm = str(inputTimes[-1])
            minutes = int(timerm[2:4])
            seconds = int(timerm[4:6])
            milliseconds = int(timerm[6:8])*10
            czas2 = datetime.timedelta(minutes=minutes, seconds=seconds, milliseconds=milliseconds)
            suma = mainTime + czas2
            mainTime = suma
            del inputTimes[-1]
            self.lista.text = 'time left: ' + str(mainTime)[2:10].replace('.', ':')
        except IndexError:
            self.lista.text = 'time left: ' + str(mainTime)[2:10].replace('.', ':')

WumpaTime().run()
