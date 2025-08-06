from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Use environment variables for secure DB connection
DB_HOST = os.environ.get("DB_HOST", "sql12.freesqldatabase.com")
DB_USER = os.environ.get("DB_USER", "sql12793821")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "1UE6ipdYba")
DB_NAME = os.environ.get("DB_NAME", "sql12793821")
DB_PORT = int(os.environ.get("DB_PORT", 3306))

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    level = request.form['level']
    dribble_speed = request.form['dribble_speed']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            level VARCHAR(100),
            dribble_speed VARCHAR(100)
        )
    ''')

    cursor.execute('''
        INSERT INTO users (name, level, dribble_speed)
        VALUES (%s, %s, %s)
    ''', (name, level, dribble_speed))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('challenge'))

@app.route('/challenge')
def challenge():
    return render_template('challenge.html')

@app.route('/responses')
def responses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('responses.html', responses=data)

if __name__ == '__main__':
    app.run(debug=True)
