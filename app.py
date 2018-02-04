from flask import Flask, abort, request, render_template
app = Flask(__name__)
app.static_folder = 'static'

@app.before_request
def limit_remote_addr():
    if request.remote_addr != '127.0.0.1':
        abort(403)  # Forbidden

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/heyhoo/')
def hello2():
    return render_template('heyhoo.html')




if __name__ == '__main__':
    app.run(debug=True)


    


