from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/b2c')
def b2c():
    # values = get_values()
    return render_template('b2c.html')

@app.route('/b2b')
def b2b():
    # values = get_values()
    return render_template('b2b.html')

if __name__ == '__main__':
    app.run(debug=True)