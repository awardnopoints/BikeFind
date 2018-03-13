from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'mytest'
mysql = MySQL(app)

@app.route("/")

def main():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * from new_table''')
    rv = cur.fetchall()
    return str(rv)

if __name__ == "__main__":
    app.run(debug=True)
