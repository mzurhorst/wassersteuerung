from flask import Flask, render_template
app = Flask(__name__)
app.static_folder = 'static'


@app.route('/')
def hello():
    return "Hello World - TesghfghIch habet 2"

@app.route('/heyhoo/')
def hello2():
    return render_template('heyhoo.html')




if __name__ == '__main__':
    app.run(debug=True)
