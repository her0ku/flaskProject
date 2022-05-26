import init_db


def send_form_to_moderation(user_id, coordinates_lon, coordinates_lat, comment, type_event, address):
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO moderation_list(user_id, coordinates, annotation, type_event,address) VALUES(%s,ST_SetSRID(ST_MakePoint(%s, %s),4326),%s,%s,%s)', (user_id, coordinates_lon, coordinates_lat, comment, type_event, str(address)))
    conn.commit()
    cur.close()
    conn.close()
