from flask import Flask, abort, request, render_template, json, jsonify

app = Flask(__name__)
app.static_folder = 'static'

@app.before_request
def limit_remote_addr():
    if request.remote_addr != '127.0.0.1':
        abort(403)  # Forbidden

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/test2')
def hello2():
    return render_template('test2.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signupuser', methods=['POST', 'GET'])
def signupuser():
    user =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/noisefloor')
def index():
    return render_template('noisefloor.html')

@app.route('/sliderdata', methods=['POST'])
def sliderdata():
    data = request.form['data']
    #do something else here if necessary
    return ('', 200)

@app.route('/numberdata', methods=['POST'])
def numberdata():
    data1 = request.json.get('value1')
    data2 = request.json.get('value2')
    length = "--"
    response='ok - got {} and {} --- Message Queue Inhalt: {}'.format(data1, data2, length)
    #do something else here, too, if necessary
    return jsonify(status=response)




class StatusMessages:
    def __init__(self, instance, max_delay):
        from random import randint
        from threading import Thread
        self.t = Thread(target=self.__worker, args=())
        self.max_delay = max_delay
        self.instance = instance
        self.delay = randint(0, self.max_delay)       
        self.statusmessage1 = "Meldung 1 von " + self.instance
        self.statusmessage2 = "Meldung 2"
        self.statusmessage3 = "Meldung 3"
        self.statusmessage4 = "Meldung 4"
        self.counter = 0
        self.__update()
        
    def add(self, newmessage):
        self.statusmessage4 = self.statusmessage3        
        self.statusmessage3 = self.statusmessage2
        self.statusmessage2 = self.statusmessage1
        self.statusmessage1 = newmessage
        #print("Nach " + str(newmessage) + " Sekunden eine Meldung hinzugefuegt.\n")
        
    def __update(self):
        self.t.start()        
        
    def __worker(self):
        import time
        from random import randint
        self.add(self.delay)
        self.counter += 1
        print(" ---- " + self.instance + " ---- Counter: " + str(self.counter) + " ----")
        print("Meldung 1: " + str(self.statusmessage1) )
        print("Meldung 2: " + str(self.statusmessage2) )
        print("Meldung 3: " + str(self.statusmessage3) )
        print("Meldung 4: " + str(self.statusmessage4) + "\n")
        time.sleep(self.delay)
        self.delay = randint(0, self.max_delay)
        from threading import Thread
        self.t = Thread(target=self.__worker, args=())  
        self.__update()
        


sm = StatusMessages("sm", 5)
sm2 = StatusMessages("sm2", 3)



if __name__ == '__main__':
    #app.run(debug=True, threaded=True)
    sm.add("Testnachricht")
    sm2.add("Nachricht aus dem zweiten Objekt")
    


