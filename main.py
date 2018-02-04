from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World - Test 2"

@app.route('/heyhoo/')
def hello2():
    return render_template('heyhoo.html')




if __name__ == '__main__':
    app.run()














#from kivy.config import Config
#Config.set('graphics',  'resizeable',  False)
#Config.set('graphics',  'width',  '800')
#Config.set('graphics',  'height',  '480')

## from kivy.core.window import Window
## Window.borderless = True

#from kivy.properties import ObjectProperty
#from kivy.app import App

#class GartenbewaesserungApp(App):
    #def  testfunktion(self,  *args):
       #print ("Testausgabe") 
       #print("Args[1] Typ = ", type(args[1]))
       #print(args[1])
       #if args[1] == "down":
           #print("Turning On")
           ##self.root.ids.popuptextinput.disabled = True  
       #else:
           #print("Turning Off")       
           ##self.ids.popuptextinput.disabled = False  
       ## exit(0)
       
       


if __name__ == '__main__':
    GartenbewaesserungApp().run()

