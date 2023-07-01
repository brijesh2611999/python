import mysql.connector
from flask import Flask, render_template, request
from mysql.connector import Error

app = Flask(__name__)
try:
    conn = mysql.connector.connect(host='localhost', database='demo', user='root', password='')

    if conn.is_connected():
        db = conn.get_server_info()
        print("connected to mysql server", db)
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("connected to", record)


        @app.route('/')
        def home():
            return render_template('login.html')


        @app.route('/about')
        def about():
            return "<i>this is about page section</i>"


        @app.route('/register')
        def register():
            return render_template('register.html')


        @app.route('/login_validation', methods=['POST'])
        def login_validation():
            email = request.form.get('email')
            password = request.form.get('password')
            cursor.execute(f"""SELECT * FROM `login` WHERE `id` LIKE '{email}' AND `password` LIKE '{password}' """)
            users = cursor.fetchall()
            sql = "INSERT INTO login (id, password) VALUES (%s,%s)"
            val = (email, password)
            cursor.execute(sql, val)
            # cursor.execute("INSERT INTO login('id','password')VALUES('{0}','{1}')".format(email,password))
            conn.commit()
            return "user registration successfully"


        if __name__ == "__main__":
            app.run(debug=True)

except Error as e:
    print("error while connecting to database", e)
