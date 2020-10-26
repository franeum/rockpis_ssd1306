#!/usr/bin/env python3

import conn 
import kivy 
import ssh_connect as ssh 
import time 
  
# base Class of your App inherits from the App class. 
# app:always refers to the instance of your application 
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
  
# this restrict the kivy version i.e 
# below this kivy version you cannot  
# use the app or software 
# not coumpulsary to write it 
kivy.require('1.11.1') 


class CredentialPopup(Popup):
    pass


class MainBox(BoxLayout): 
    # For Spinner defining spinner clicked function 

    def spinner_clicked(self, value):
        self.ssid = value  
        print("Language selected is " + value) 

    def print_pwd(self, value):
        self.pwd = value 

    def credential_send(self):
        #try:
        print("le credenziali sono: ", self.ssid, self.pwd)
        timestamp = time.time()
        res = ssh.send_credential(self.ssid, self.pwd, timestamp)
        print(res)
        if res == 0:
            pop = CredentialPopup()
            pop.open()
        else:
            print("stocazzo")
        #except:
            #print("You have to choose a network and tell a password")



class MyLabel(Label):
    def format_text(self, txt):
        return '[color=#88e5af][b]' + txt + '[/b][/color]'


class kvfileApp(App): 
    networks = conn.enumerate_wifi(conn.get_available_wifi()) 
    networks = [x[1] for x in networks]
    def build(self):
        return MainBox()

  
kv = kvfileApp() 
kv.run() 