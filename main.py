from flask import Flask, render_template
from values import calculate_stats
from datetime import datetime

app = Flask(__name__)

# @app.route('/')
# @app.route('/index')
# def index():
#     current_date = datetime.today().strftime("%d.%m.%Y")
    
#     return render_template('index.html', current_date = current_date)

# @app.route('/b2c')
# def b2c():
#     current_date = datetime.today().strftime("%d.%m.%Y")

#     values = calculate_stats(department = 'b2c')
#     values['total'] = round(values['total'], 2)

#     return render_template('b2c.html', values = values, current_date = current_date)

@app.route('/')
@app.route('/index')
@app.route('/b2b')
def b2b():
    current_date = datetime.today().strftime("%d.%m.%Y")

    values = calculate_stats(department = 'b2b')
    values['total_created'] = round(values['total_created'], 2)
    values['total_won'] = round(values['total_won'], 2)
    values['forecast'] = round(values['forecast'], 2)

    return render_template('b2b.html', values = values, current_date = current_date)

if __name__ == '__main__':
    app.run(debug=True)
