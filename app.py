from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

# Database connection function using environment variables
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME'),
        port=int(os.environ.get('DB_PORT', 3306))
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    level = request.form['level']
    dribble_speed = request.form['dribble_speed']
    challenge_response = request.form['challenge_response']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            level VARCHAR(100),
            dribble_speed VARCHAR(100),
            challenge_response VARCHAR(10)
        )
    ''')
    cursor.execute('''
        INSERT INTO users (name, level, dribble_speed, challenge_response)
        VALUES (%s, %s, %s, %s)
    ''', (name, level, dribble_speed, challenge_response))
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('thankyou.html')

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
