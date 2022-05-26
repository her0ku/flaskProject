from flask import Flask, render_template, request, session
import os
import asyncio
import getCoordinates
import mapEngine
import init_db
import datetime
import bcrypt
import secrets
from sqlLogin import create_user, find_user_by_mail, find_user_by_id
from sqlCommands import send_form_to_moderation, get_info_data

token = secrets.token_urlsafe(16)
app = Flask(__name__)
app.config["SECRET_KEY"] = token


@app.get('/')
async def index():
    my_name = session.get('USERNAME')
    return render_template('startView.html', my_name=my_name)


@app.route('/registration', methods=['GET', 'POST'])
async def reg_page():
    if request.method == 'GET':
        return render_template('registration.html')
    if request.method == 'POST':
        last_name = request.form['last-name']
        first_name = request.form['first-name']
        nickname = request.form['nickname']
        phone = request.form['phone']
        mail = request.form['mail']
        country = request.form['country']
        city = request.form['city']
        date_birth = request.form['date-birth']
        date_now = datetime.datetime.now().date()
        year = date_birth[0:4]
        age = datetime.datetime.now().date().year - int(year)
        password = request.form['pass'].encode('UTF-8')
        bpassword = bcrypt.hashpw(password, bcrypt.gensalt(16)).decode()
        create_user(first_name, last_name, mail, date_birth, phone, nickname, bpassword, date_now, country, city, age)
        session['USERNAME'] = nickname
        return render_template('startView.html', my_name=session['USERNAME'])


@app.route('/login', methods=['GET', 'POST'])
async def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['pass']
        bpass = find_user_by_mail(mail)
        if bcrypt.checkpw(password.encode('utf8'), bpass.encode('UTF-8')):
            session['USERNAME'] = mail
            return render_template('startView.html', my_name=session['USERNAME'])
        else:
            return render_template('login.html')


@app.route('/moderation', methods=['GET', 'POST'])
async def send_to_moderation():
    if request.method == 'GET':
        #if session.get('USERNAME') is None:
            #return render_template('login.html')
        return render_template('moderationForm.html')
    if request.method == 'POST':
        name = session['USERNAME']
        user_id = find_user_by_id(name)
        address = request.form['address']
        coordinates_lon, coordinates_lat = getCoordinates.get_coordinates(address)
        type_event = request.form['type']
        comment = request.form['comment']
        print(coordinates_lon, coordinates_lat)
        #send_form_to_moderation(user_id, coordinates_lon, coordinates_lat, comment, type_event, address)
        return 'a'


@app.get('/connection')
async def connector():
    result = init_db.get_conn()
    cur = result.cursor()
    cur.execute('SELECT * FROM users;')
    res = cur.fetchall()
    print(res)
    cur.close()
    result.close()
    return 'OK'


@app.post('/route')
async def my_route():
    route_1 = request.form['coord1']
    route_2 = request.form['coord2']
    location1 = getCoordinates.get_location(route_1)
    location2 = getCoordinates.get_location(route_2)
    mapEngine.calculate_route(location1, location2)
    return render_template('results.html')


@app.get('/marks')
async def my_mark():
    mapEngine.add_custom_mark()
    return render_template('marks.html')


@app.get('/data')
async def my_data():
    res = get_info_data()
    print(res)
    return 'res'


if __name__ == '__main__':
    app.run()