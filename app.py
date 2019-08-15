from flask import Flask
from flask import render_template, request, redirect, url_for, flash
import sqlite3
from flask_json import FlaskJSON, json_response
import subprocess
from sys import platform
from datetime import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
flaskjson = FlaskJSON(app)
cors = CORS(app)
app.secret_key = b'10a6b4abc946ee7b91aa534a3bf02f3ac5d9a67c126c030464bc4d5f244f7256'
app.config['CORS_HEADERS'] = 'Content-Type'

logger = app.logger
DBNAME = 'tbgs.db'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getGroups')
@cross_origin()
def get_groups():
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute('select groupname, shotcount from shotmeter order by shotcount desc')
    group_data = cursor.fetchall()

    return_data = []

    for group in group_data:
        print(group)
        datapoint = {'y': group[1], 'label': group[0]}
        return_data.append(datapoint)

    # print(return_data)

    return json_response(data=return_data)


@app.route('/enter')
@app.route('/eintrag')
@app.route('/eingabe')
def enter():
    conn = sqlite3.connect(DBNAME)
    grps = conn.execute('select groupname from shotmeter')
    groups = grps.fetchall()
    print(groups)
    return render_template('enter.html', groups=groups)


@app.route('/shutdown', methods=['GET', 'POST'])
@app.route('/ausschalten', methods=['GET', 'POST'])
@app.route('/herunterfahren', methods=['GET', 'POST'])
def shutdown():
    if request.method == 'POST':
        if platform == "linux" or platform == "linux2":
            command = "/usr/bin/sudo /sbin/shutdown -h now"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output = process.communicate()[0]
        else:
            print('on linux i would shutdown now')
        flash('Shotstand wird heruntergefahren.')
        return render_template('shutdown.html')
    else:
        return render_template('shutdown.html')

@app.route('/safe', methods=['POST'])
def safe():
    groupname = request.form['groupname']
    addcount = request.form['shotcount']

    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()

    cursor.execute("select * from shotmeter where groupname = '{}' LIMIT 1".format(groupname))
    rows = cursor.fetchall()
    # print(rows)

    if len(rows) > 0:
        newshots = int(rows[0][2]) + int(addcount)
        sql = "update shotmeter set shotcount = {newshots} where groupname = '{groupname}'".format(newshots=newshots,
                                                                                                   groupname=groupname)
    else:
        sql = "insert into shotmeter (groupname, shotcount) values ('{groupname}', '{shotcount}')".format(
            groupname=groupname,
            shotcount=addcount)

    if cursor.execute(sql):
        conn.commit()
        flash("{shots} Shots für {groupname} hinzugefügt.".format(shots=addcount, groupname=groupname))
    else:
        flash("Fehler beim speichern, bitte noch einmal versuchen.")

    today = datetime.now()
    cursor.execute(
        "insert into analytics (groupname, shots_bougth, timestamp) values ('{groupname}',{shots},'{timestamp}')".format(
            groupname=groupname,
            shots=int(addcount),
            timestamp=today))
    conn.commit()
    cursor.close()
    conn.close()

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


@app.before_first_request
def initalizer():
    # logging.debug('running initializer')
    conn = sqlite3.connect(DBNAME)
    conn.execute('CREATE TABLE IF NOT EXISTS shotmeter ('
                 'id INTEGER PRIMARY KEY, '
                 'groupname TEXT not null , '
                 'shotcount INTEGER'
                 ')')
    conn.execute('CREATE TABLE IF NOT EXISTS analytics('
                 'id INTEGER PRIMARY KEY,'
                 'groupname TEXT NOT NULL,'
                 'shots_bougth INTEGER NOT NULL,'
                 'timestamp TEXT NOT NULL'
                 ')')
    conn.close()


if __name__ == '__main__':
    
    import logging
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run()
