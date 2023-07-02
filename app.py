import json

from flask import Flask, render_template, request, session, make_response
import os
import asyncio
import getCoordinates
import mapEngine
import init_db
import datetime
import bcrypt
import secrets
from flask_cors import CORS, cross_origin
from sqlLogin import create_user, find_user_by_mail, find_user_id, find_user_by_id, find_role_id, set_user_role, find_user_role
from sqlCommands import send_form_to_moderation, get_info_data, delete_info_card, accept_info_card, get_info_accepted_data
from geopy.geocoders import Nominatim


token = secrets.token_urlsafe(16)
app = Flask(__name__)
app.config["SECRET_KEY"] = token
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
geolocator = Nominatim(user_agent="http")


@app.get('/startPage')
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
        id = find_user_id(mail)
        session["USERNAME"] = mail
        set_user_role(id)
        return render_template('startView.html', my_name=session['USERNAME'])


@app.route('/', methods=['GET', 'POST'])
async def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['pass']
        bpass = find_user_by_mail(mail)
        user_id = find_user_id(mail)
        user_role = find_user_role(user_id)
        if bcrypt.checkpw(password.encode('utf8'), bpass.encode('UTF-8')):
            session['USERNAME'] = mail
            if user_role == 'user':
                return render_template('startView.html', my_name=session['USERNAME'])
            elif user_role == 'moderator':
                return render_template('moderatorViewer.html', my_name=session['USERNAME'])
        else:
            return render_template('login.html')

@app.route('/tests', methods=['GET'])
async def tesss():
    return 'aaaaaaaaaaaa'

@app.route('/moderation', methods=['GET', 'POST'])
async def send_to_moderation():
    if request.method == 'GET':
        if session.get('USERNAME') is None:
            return render_template('login.html')
        return render_template('moderationForm.html')
    if request.method == 'POST':
        name = session['USERNAME']
        user_id = find_user_id(name)
        address = request.form['address']
        coordinates_lon, coordinates_lat = getCoordinates.get_coordinates(address)
        type_event = request.form['type']
        comment = request.form['comment']
        status = 'проверка'
        send_form_to_moderation(user_id, coordinates_lon, coordinates_lat, comment, type_event, address, status)
        return render_template('moderationForm.html')


@app.get('/moderatorView')
async def card_view():
    data = list(get_info_data())
    for i in data:
        user_name = find_user_by_id(i[1])
        i.append(user_name)
    return render_template('moderatorViewer.html', card_info=data)


@app.route("/moderatorView/delete/<int:id>", methods=["DELETE"])
async def delete_card(id):
    delete_info_card(id)
    return render_template('moderatorViewer.html')


@app.route('/moderatorView/add/<int:id>', methods=['POST'])
async def add_form(id):
    accept_info_card(id)
    return render_template('moderatorViewer.html')


@app.post('/route')
async def my_route():
    route_1 = request.form['coord1']
    route_2 = request.form['coord2']
    location1 = getCoordinates.get_location(route_1)
    location2 = getCoordinates.get_location(route_2)
    mapEngine.calculate_route(location1, location2)
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('results.html'), 200, headers)


@app.route('/coordinates', methods=['POST'])
async def get_coordinates():
    route_1 = request.form['coord1']
    route_2 = request.form['coord2']
    location1 = getCoordinates.get_location(route_1)
    location2 = getCoordinates.get_location(route_2)
    data = parse_coordinates(location1, location2)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.post('/getAddress')
async def get_address():
    req = request.get_json()
    res = req['coord1']
    lat, lon = res
    print(lat, lon)
    #data = getCoordinates.get_address_from_coordinates(latitude, longitude)
    #response = app.response_class(
    #    response=json.dumps(data),
    #    status=200,
    #    mimetype='application/json'
    #)
    return 'response'

@app.get('/marks')
async def my_mark():
    data = list(get_info_accepted_data())
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
