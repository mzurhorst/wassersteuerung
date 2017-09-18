from kivy.config import Config
Config.set('graphics',  'resizeable',  False)
Config.set('graphics',  'width',  '800')
Config.set('graphics',  'height',  '480')

# from kivy.core.window import Window
# Window.borderless = True

from kivy.app import App

class GartenbewaesserungApp(App):
    def  testfunktion(self,  *args):
       print ("Testausgabe") 
       if args[1]:
           self.Status1 = "Device On"
           print("Turning On")
       else:
           self.Status1 = "Device Off"
           print("Turning Off")       
       # exit(0)


if __name__ == '__main__':
    
    GartenbewaesserungApp().run()

