from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Maharshi@2004',  # 🔁 Replace with your actual MySQL password
        database='football_challenge'
    )

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        level = request.form['level']
        dribble_time = request.form['dribble_time']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, level, dribble_time) VALUES (%s, %s, %s)",
            (name, level, dribble_time)
        )
        user_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('challenge', user_id=user_id))

    return render_template('login.html')

@app.route('/challenge/<int:user_id>', methods=['GET', 'POST'])
def challenge(user_id):
    if request.method == 'POST':
        response = request.form['response']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET response = %s WHERE id = %s",
            (response, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return (
            "<h2 style='text-align:center;'>Thanks for responding! 🔥</h2>"
            "<h3 style='text-align:center;'>Meet You Tomorrow Eve 5:00pm @Rymec Ground</h3>"
        )

    return render_template('challenge.html', user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
