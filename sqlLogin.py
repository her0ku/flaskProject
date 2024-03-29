import init_db


def create_user(first_name, last_name, mail, date_birth, phone, nickname, bpassword, date_now, country, city, age):
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('SELECT email, user_name FROM users WHERE email = %s OR user_name = %s', (mail, nickname, ))
    if cur.fetchone() is None:
        cur.execute(
            'INSERT INTO users (first_name, last_name, email, date_birth, phone, user_name, password, created_date, country, city, age ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (first_name, last_name, mail, date_birth, phone, nickname, bpassword, date_now, country, city, age))
        conn.commit()
    else:
        return False
    cur.close()
    conn.close()


def set_user_role(user_id):
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO rolesid(user_id, role_id) VALUES(%s,%s)', (user_id, 1))
    conn.commit()
    cur.close()
    conn.close()


def find_role_id(id):
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('SELECT role_id FROM rolesid WHERE user_id = %s', (id, ))
    role_id = cur.fetchone()[0]
    return role_id


def find_user_role(id):
    conn = init_db.get_conn()
    cur = conn.cursor()
    role_id = find_role_id(id)
    cur.execute('SELECT user_role from roles, rolesid WHERE rolesid.user_id = %s AND roles.role_id = %s', (id, role_id))
    return cur.fetchone()[0]


def find_user_by_mail(mail):
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('SELECT email, password FROM users WHERE email = %s', (mail, ))
    return cur.fetchone()[1]


def find_user_by_id(id):
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('SELECT user_name FROM users WHERE user_id = %s', (id, ))
    return cur.fetchone()[0]


def find_user_id(mail):
    conn = init_db.get_conn()
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM users WHERE email = %s', (mail, ))
    id = cur.fetchone()[0]
    return id
