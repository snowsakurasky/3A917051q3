from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = '123456789'

@app.route("/")
def index():
    try:
        if 'username' in session:
            username = session['username']
            conn = sqlite3.connect('mydb.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM member WHERE phone = ?', (username,))
            user = cursor.fetchone()
            return render_template('index.html', user=user)
        else:
            return render_template('login.html')
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(str(e))
        return render_template("error.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "GET":
            return render_template("login.html")
        elif request.method == "POST":
            idno = request.form.get("idno")
            pwd = request.form.get("pwd")

            conn = sqlite3.connect('mydb.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM member WHERE idno = ?', (idno,))
            user = cursor.fetchone()

            if user and user['pwd'] == pwd:
                session['username'] = user['phone']
                return redirect(url_for('index'))
            else:
                return render_template("login.html", error="請輸入正確的帳號密碼")
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(str(e))
        return render_template("error.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    try:
        if 'username' not in session:
            return redirect(url_for('login'))

        username = session['username']
        conn = sqlite3.connect('mydb.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if request.method == "POST":
            nm = request.form.get('nm')
            birth = request.form.get('birth')
            blood = request.form.get('blood')
            phone = request.form.get('phone')
            email = request.form.get('email')
            idno = request.form.get('idno')
            pwd = request.form.get('pwd')

            cursor.execute('''UPDATE member SET nm = ?, birth = ?, blood = ?, phone = ?
                           , email = ?, idno = ?,  pwd= ? WHERE phone = ?''',
                           (nm, birth, blood, phone, email, idno, pwd, username))
            conn.commit()

            return redirect(url_for('index'))
        cursor.execute('SELECT * FROM member WHERE phone = ?', (username,))
        user = cursor.fetchone()
        return render_template("edit.html", user=user)
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(str(e))
        return render_template("error.html")



@app.route("/logout")
def logout():
    try:
        session['username'] =''
        return redirect(url_for('login'))
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(str(e))
        return render_template("error.html")




