from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
from flask import session
import os
os.urandom(24)

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'chemchat_db'
app.config['MYSQL_PORT'] = 3307
app.secret_key = b'\xf3\x1c\xa2\xe4\x81\xdf\x89\xbb\xd2\xf9\xa1\xfb\xf9\xc8\x12\x1b\x9c\x88\x0c\xaa'


mysql = MySQL(app)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()
    
    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cur.execute(query, (username, email, password))
    
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']

    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        session['user_ID'] = user[0]
        return redirect(url_for('custo_page'))
    else:
        return "Invalid login credentials"

@app.route('/user_dt', methods=["POST"])
def user_dt():
    user_ID = session.get('user_ID')

    if not user_ID:
        return redirect(url_for('signin'))

    name = request.form.get('name')
    nickname = request.form.get('nickname')
    age = request.form.get('age')
    chat_preference = request.form.get('preference')

    cur = mysql.connection.cursor()

    query = "UPDATE users SET name = %s, nickname = %s, age = %s, chat_preference = %s WHERE ID = %s"
    cur.execute(query, (name, nickname, age, chat_preference, user_ID))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('chat_page'))
    
@app.route('/custo_page')
def custo_page():
    return render_template('Custo_Page.html')

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/chat_page')
def chat_page():
    return render_template('Chat_Page.html')

if __name__ == '__main__':
    app.run(debug=True)
