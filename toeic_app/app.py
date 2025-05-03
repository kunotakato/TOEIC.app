from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'scores.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            listening_score INTEGER,
            reading_score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        listening = int(request.form['listening_score'])
        reading = int(request.form['reading_score'])
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('INSERT INTO scores (date, listening_score, reading_score) VALUES (?, ?, ?)',
                  (date, listening, reading))
        conn.commit()
        conn.close()
        return redirect('/')

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT date, listening_score, reading_score FROM scores ORDER BY date')
    data = c.fetchall()
    conn.close()

    dates = [row[0] for row in data]
    listening_scores = [row[1] for row in data]
    reading_scores = [row[2] for row in data]
     # 合計スコアの計算を追加
    total_scores = [l + r for l, r in zip(listening_scores, reading_scores)]

    return render_template('index.html',
                           dates=dates,
                           listening_scores=listening_scores,
                           reading_scores=reading_scores,
                           total_scores=total_scores)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
