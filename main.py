from flask import Flask,render_template,redirect,request
import sqlite3
from datetime import datetime as dt

app = Flask(__name__)

def connection_():
    conn = sqlite3.connect('device_values.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS journal (
id INTEGER PRIMARY KEY,
duty TEXT NOT NULL,
date TEXT NOT NULL, 
motoclock_dgu TEXT NOT NULL,
temp_dgu TEXT NOT NULL,
voltage_dgu TEXT NOT NULL,
temp_spk TEXT NOT NULL,
humidity TEXT NOT NULL,
voltage_ov TEXT NOT NULL,
voltage_db TEXT NOT NULL
)
    ''')
    conn.commit()
    conn.close()

def get_all_posts():
    conn = sqlite3.connect('device_values.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM journal')
    all_posts = cursor.fetchall()
    return all_posts


def get_all_posts_date(date):
    conn = sqlite3.connect('device_values.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM journal WHERE date = '{date}'")
    all_posts_date = cursor.fetchall()
    return all_posts_date

connection_()
current_date = dt.now()


@app.route('/')
@app.route('/index/')
def route():
    return render_template('index.html')

@app.route('/add_values', methods=['POST', 'GET'])
def add_values():
    if request.method == 'POST':
        date = request.form.get('date')
        motoclock_dgu = request.form.get('motoclock')
        temp_dgu = request.form.get('temp')
        voltage_dgu = request.form.get('voltage')
        temp_spk = request.form.get('temp_spk')
        humidity = request.form.get('humidity')
        voltage_ov = request.form.get('voltage_ov')
        voltage_db = request.form.get('voltage_db')
        duty = request.form.get('duty')


        try:
            sqlite_connection = sqlite3.connect('device_values.db')
            cursor = sqlite_connection.cursor()
            cursor.execute(f'''INSERT INTO journal (date, motoclock_dgu, temp_dgu, voltage_dgu, temp_spk, humidity,voltage_ov,voltage_db,duty) VALUES 
            ('{date}','{motoclock_dgu}','{temp_dgu}','{voltage_dgu}','{temp_spk}','{humidity}','{voltage_ov}','{voltage_db}','{duty}')''')
            sqlite_connection.commit()
            print(f"Запись успешно вставлена в таблицу, количество вставлено: ", cursor.rowcount)
            cursor.close()
            return redirect('/all_posts')
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
    else:
        return render_template('add_values.html', current_date=current_date)

@app.route('/all_posts')
def all_posts():
    result = get_all_posts()
    return render_template('/all_posts.html', result=result)

@app.route('/spk')
def spk():
    return render_template('spk.html')

@app.route('/asgpt')
def asgpt():
    return render_template('asgpt.html')

@app.route('/dgu')
def dgu():
    return render_template('dgu.html')

@app.route('/electro')
def electro():
    return render_template('electro.html')

@app.route('/ibp')
def ibp():
    return render_template('ibp.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        date = request.form.get('date')
        result = get_all_posts_date(date)
        return render_template('search.html', result = result)
    else:
        return render_template('search.html',result = [''])
if __name__ == '__main__':
    app.run(debug=True)

