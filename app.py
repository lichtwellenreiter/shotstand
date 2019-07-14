from flask import Flask
from flask import render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = b'10a6b4abc946ee7b91aa534a3bf02f3ac5d9a67c126c030464bc4d5f244f7256'
DBNAME = 'tbgs.db'


@app.route('/')
def index():
    return render_template('index.html', msgcount="98632964")


@app.route('/enter')
@app.route('/eintrag')
@app.route('/eingabe')
def enter():
    conn = sqlite3.connect(DBNAME)
    grps = conn.execute('select groupname from shotmeter')
    groups = grps.fetchall()
    return render_template('enter.html', groups=groups)


@app.route('/safe', methods=['POST'])
def safe():
    groupname = request.form['groupname']
    addcount = request.form['shotcount']

    conn = sqlite3.connect(DBNAME)
    # sql = "update shotmeter set count = count + {addcount} where groupname = '{groupname}'".format(addcount=addcount,
    # groupname=groupname)

    sql = "insert or replace into shotmeter (groupname, shotcount) values ('{groupname}', shotcount + {addcount})".format(
        groupname=groupname, addcount=addcount)

    print(sql)

    conn.execute(sql)
    flash("Anzahl gespeichert für {}".format(groupname))
    return redirect(url_for('enter'))


@app.errorhandler(500)
def handle_500(error):
    return render_template('views/errors/error.html', error=error, errornum=500), 500


@app.errorhandler(404)
def handle_404(error):
    return render_template('views/errors/error.html', error=error, errornum=404), 404


@app.errorhandler(405)
def handle_405(error):
    return render_template('views/errors/error.html', error=error, errornum=405), 405


if __name__ == '__main__':
    conn = sqlite3.connect(DBNAME)
    conn.execute(
        'CREATE TABLE IF NOT EXISTS shotmeter (id INTEGER PRIMARY KEY, groupname TEXT not null , shotcount INTEGER)')
    app.run()
    conn.close()
