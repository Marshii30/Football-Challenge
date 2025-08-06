from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='sql12.freesqldatabase.com',
        user='sql12793821',
        password='1UE6ipdYba',
        database='sql12793821',
        port=3306
    )

# Home page with form
@app.route('/')
def index():
    return render_template('index.html')

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    level = request.form['level']
    dribble_speed = request.form['dribble_speed']
    challenge_response = request.form['challenge_response']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            level VARCHAR(100),
            dribble_speed VARCHAR(100),
            challenge_response VARCHAR(10)
        )
    ''')

    # Insert data
    cursor.execute('''
        INSERT INTO users (name, level, dribble_speed, challenge_response)
        VALUES (%s, %s, %s, %s)
    ''', (name, level, dribble_speed, challenge_response))

    conn.commit()
    cursor.close()
    conn.close()

    return render_template('thankyou.html')

# Show all responses (for admin/testing)
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
