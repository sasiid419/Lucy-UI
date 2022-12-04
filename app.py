

import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='127.0.0.1',
                            port = '5432',
                            database='Lucy-new',
                            user=os.getenv('DBun'),
                            password=os.getenv('DBps'))
    return conn


@app.route('/',  methods=('GET', 'POST'))
def index():
    col = []
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        transaction = request.form.get('transaction')
        if transaction is not None:
            query = 'SELECT * FROM payments where transaction_id =\'' + transaction + '\';'
            cur.execute(query)
        else:
            transaction = request.form['id']
            query = 'DELETE FROM payments where transaction_id =\'' + transaction + '\';'
            cur.execute(query)
            query = 'SELECT * FROM payments where transaction_id =\'' + transaction + '\';'
            cur.execute(query)
            conn.commit()
    else:
        cur.execute('SELECT * FROM payments order by payment_timestamp desc limit 10;')
    column_names = [desc[0] for desc in cur.description]
    for i in column_names:
        col.append(i)
        # print(i)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', data=data, col=column_names)


@app.route('/refunds/',  methods=('GET', 'POST'))
def refunds():
    col = []
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        transaction = request.form['transaction']
        query = 'SELECT * FROM refunds where transaction_id =\'' + transaction + '\';'
        cur.execute(query)
    else:
        cur.execute('SELECT * FROM refunds limit 10;')
    column_names = [desc[0] for desc in cur.description]
    for i in column_names:
        col.append(i)
        # print(i)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('refunds.html', data=data, col=column_names)

@app.route('/users/',  methods=('GET', 'POST'))
def users():
    col = []
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        user = request.form['user']
        query = 'SELECT * FROM users where mail_id =\'' + user + '\';'
        cur.execute(query)
    else:
        cur.execute('SELECT * FROM users limit 10;')
    column_names = [desc[0] for desc in cur.description]
    for i in column_names:
        col.append(i)
        # print(i)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('users.html', data=data, col=column_names)
# ...


# ...

@app.route('/search/', methods=('GET', 'POST'))
def search():
    col = []
    if request.method == 'POST' :
        query = request.form['query']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query)
        column_names = [desc[0] for desc in cur.description]
        for i in column_names:
           col.append(i)
           # print(i)
        data = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        try:
            return render_template('result.html', data=data, col=column_names)
        except SyntaxError:
            print(query)

    return render_template('search.html')

@app.route('/create/', methods=('GET', 'POST'))
def create():
    col = []
    if request.method == 'POST':
        transactionId = request.form['transactionId']
        storeId = request.form['storeId']
        category = request.form['category']
        emailId = request.form['emailId']
        amount = request.form['amount']
        state = request.form['state']
        query = 'INSERT INTO payments(transaction_id, user_id, state, store_id, category, payment_instrument, payment_timestamp, amount) VALUES (\'' + transactionId + '\', (select user_id from users where mail_id = \''+ emailId + '\'), \''+ state + '\',\''+ storeId + '\',\'' + category + '\', \'ACCOUNT\',\'now()\', '+ amount +');'
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        query = 'SELECT * FROM payments where transaction_id =\'' + transactionId + '\';'
        cur.execute(query)
        column_names = [desc[0] for desc in cur.description]
        for i in column_names:
           col.append(i)
           # print(i)
        data = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        try:
            return render_template('result.html', data=data, col=column_names)
        except SyntaxError:
            print(query)

    return render_template('create.html')


if __name__ == "__main__":  # There is an error on this line
    app.run(debug=True, host='0.0.0.0')
    print("test")