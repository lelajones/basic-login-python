# main.py

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase

class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    phone = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        # validating a correct name and phone format
        if self.username.text != "": # (add phone validation) and self.phone.text != "" and self.phone.text.count("@") == 1 and self.phone.text.count(".") > 0:
            # validating a correct pw format/not blank
            if self.password != "":
                # if given info correct, add user to db
                db.add_user(self.phone.text, self.password.text, self.username.text)

                # reset field
                self.reset()

                # change window to login window
                sm.current = "login"
            else:
                # allows for different popup windows - "this is wrong with your pw"
                invalidForm()
        else:
            # allows for popup window - "name or phone number invalid"
            invalidForm()

    def login(self):
        # reset the object properties
        self.reset()
        # changes page to login window
        sm.current = "login"

    def reset(self):
        # reset the object properties so the fields are blank when we return to the screen
        self.phone.text = ""
        self.password.text = ""
        self.username.text = ""


class LoginWindow(Screen):
    phone = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        # validates username against the pw
        if db.validate(self.phone.text, self.password.text):
            # sets current user in main window to display info for current user from db
            MainWindow.current = self.phone.text
            self.reset() # resetting the form
            # takes you to main page
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset() # resetting the form
        sm.current = "create"

    def reset(self):
        self.phone.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    phone = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Name: " + name
        self.phone.text = "Phone Number: " + self.current
        self.created.text = "Created On: " + created


class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Invalid information entered. Please try again.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()

kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyMainApp().run()