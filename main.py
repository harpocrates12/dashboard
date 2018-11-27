from flask import Flask, render_template
from values import calculate_stats
from datetime import datetime
from constants import month_names

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

    current_month_key = int(datetime.today().month)
    previous_month_key = current_month_key - 1
    following_month_key = 1 if current_month_key == len(month_names) else current_month_key + 1

    months = {
        'previous'  : month_names[previous_month_key],
        'current'   : month_names[current_month_key],
        'following' : month_names[following_month_key]
    }

    values = calculate_stats(department = 'b2b')
    for val in values:
        values[val]['total_created'] = round(values[val]['total_created'], 2)
        values[val]['total_won'] = round(values[val]['total_won'], 2)
        values[val]['total_expected'] = round(values[val]['total_expected'], 2)

    # values = sorted(values.items(), key = lambda t: t[1])
    values = dict(sorted(values.items()))

    return render_template('b2b.html', values = values, current_date = current_date, months = months)

if __name__ == '__main__':
    app.run(debug=True)
