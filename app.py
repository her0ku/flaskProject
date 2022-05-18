from flask import Flask, render_template, request, Markup
import os
import asyncio
import getCoordinates
import mapEngine
import init_db

app = Flask(__name__)


@app.get('/')
async def index():
    return render_template('startView.html')


@app.get('/registration')
async def view_registrartion_page():
    return render_template('registration.html')


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


@app.post('/connection')
async def registration():
    last_name = request.form['last-name']
    first_name = request.form['first-name']
    nikname = request.form['nickname']
    phone = request.form['phone']
    mail = request.form['mail']
    print(last_name, first_name, nikname, mail, phone)
    return 'CONFIRM'


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


if __name__ == '__main__':
    app.run()