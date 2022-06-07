import init_db


def send_form_to_moderation(user_id, coordinates_lon, coordinates_lat, comment, type_event, address, status):
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO moderation_list(user_id, coordinates, annotation, type_event,address, status) VALUES(%s,ST_SetSRID(ST_MakePoint(%s, %s),4326),%s,%s,%s, %s)', (user_id, coordinates_lon, coordinates_lat, comment, type_event, str(address), status))
    conn.commit()
    cur.close()
    conn.close()


def get_info_data():
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('SELECT monitoring_id, user_id, annotation, type_event, address, ST_Y(coordinates), ST_X(coordinates) FROM moderation_list')
    data = map(list, list(cur.fetchall()))
    conn.commit()
    cur.close()
    conn.close()
    return data


def get_info_accepted_data():
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('SELECT ST_Y(coordinates), ST_X(coordinates), annotation, type_event, address FROM accept_moderation_list')
    data = map(list, list(cur.fetchall()))
    conn.commit()
    cur.close()
    conn.close()
    return data


def delete_info_card(card_id):
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM moderation_list WHERE monitoring_id = %s', (card_id, ))
    conn.commit()
    cur.close()
    conn.close()


def accept_info_card(card_id):
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('UPDATE moderation_list SET status = %s WHERE monitoring_id = %s', ('подтверждено', card_id, ))
    conn.commit()
    cur.close()
    conn.close()