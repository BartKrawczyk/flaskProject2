from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pandas as pd
import numpy as np
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1234567890'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)




# http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pythonlogin.accounts WHERE username = %s AND password = %s',
                       (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)

    # =================================Service Start=========================================
    #Ludność
    df = pd.read_csv('./static/LUDN.csv', sep=';', decimal=',')
    df.drop(df.columns[[0, 17]], axis=1, inplace=True)

    df.rename(columns={"ogółem;ogółem;2017;[osoba]": 'ogółem_2017'
        , 'ogółem;ogółem;2018;[osoba]': 'ogółem_2018'
        , 'ogółem;ogółem;2019;[osoba]': 'ogółem_2019'
        , 'ogółem;ogółem;2020;[osoba]': 'ogółem_2020'
        , 'ogółem;ogółem;2021;[osoba]': 'ogółem_2021'
        , 'ogółem;mężczyźni;2017;[osoba]': 'mężczyźni_2017'
        , 'ogółem;mężczyźni;2018;[osoba]': 'mężczyźni_2018'
        , 'ogółem;mężczyźni;2019;[osoba]': 'mężczyźni_2019'
        , 'ogółem;mężczyźni;2020;[osoba]': 'mężczyźni_2020'
        , 'ogółem;mężczyźni;2021;[osoba]': 'mężczyźni_2021'
        , 'ogółem;kobiety;2017;[osoba]': 'kobiety_2017'
        , 'ogółem;kobiety;2018;[osoba]': 'kobiety_2018'
        , 'ogółem;kobiety;2019;[osoba]': 'kobiety_2019'
        , 'ogółem;kobiety;2020;[osoba]': 'kobiety_2020'
        , 'ogółem;kobiety;2021;[osoba]': 'kobiety_2021'}, inplace=True)
    sum_2018 = np.sum(df['ogółem_2018'] / 1000000).round(decimals=4)
    sum_2019 = np.sum(df['ogółem_2019'] / 1000000).round(decimals=4)
    sum_2020 = np.sum(df['ogółem_2020'] / 1000000).round(decimals=4)
    sum_2021 = np.sum(df['ogółem_2021'] / 1000000).round(decimals=4)
    k_2018 = np.sum(df['mężczyźni_2018'] / 1000000).round(decimals=4)
    k_2019 = np.sum(df['mężczyźni_2019'] / 1000000).round(decimals=4)
    k_2020 = np.sum(df['mężczyźni_2020'] / 1000000).round(decimals=4)
    k_2021 = np.sum(df['mężczyźni_2021'] / 1000000).round(decimals=4)
    m_2018 = np.sum(df['kobiety_2018'] / 1000000).round(decimals=4)
    m_2019 = np.sum(df['kobiety_2019'] / 1000000).round(decimals=4)
    m_2020 = np.sum(df['kobiety_2020'] / 1000000).round(decimals=4)
    m_2021 = np.sum(df['kobiety_2021'] / 1000000).round(decimals=4)

    lab = df['Nazwa']
    values1 = df['ogółem_2018']
    values2 = df['ogółem_2019']
    values3 = df['ogółem_2020']
    values4 = df['ogółem_2021']

    figure(figsize=(13, 6), dpi=72)
    width = 0.16
    index = np.arange(len(lab))
    plt.title('Ludność z podziałem na województwa w latach 2018-2021')
    plt.bar(index - 0.25, values1, width, label='Rok_2018')
    plt.bar(index - 0.09, values2, width, label='Rok_2019')
    plt.bar(index + 0.08, values3, width, label='Rok_2020')
    plt.bar(index + 0.25, values4, width, label='Rok_2021')
    plt.xticks(ticks=range(16), labels=lab, rotation=70)
    plt.legend()
    # plt.show()
    plt.savefig('./static/img/001')
    plt.close()
    # In[560]:

    lab2 = (('2018'), ('2019'), ('2020'), ('2021'))
    figure(figsize=(13, 6), dpi=72)
    plt.yticks(np.arange(0, 40, 1))
    width = 0.2
    index = 0
    plt.title('Ludność w kraju w latach 2018-2021')
    plt.bar(index, sum_2018, width, label='Rok_2018')
    plt.bar(index + 1, sum_2019, width, label='Rok_2019')
    plt.bar(index + 2, sum_2020, width, label='Rok_2020')
    plt.bar(index + 3, sum_2021, width, label='Rok_2021')
    plt.xticks(ticks=range(4), labels=lab2, rotation=70)
    plt.legend()
    # plt.show()
    plt.savefig('./static/img/002')

    # In[561]:

    figure(figsize=(13, 6), dpi=72)
    plt.yticks(np.arange(0, 40, 1))
    width = 0.2
    index = 0
    plt.title('Wykres populacji kobiet w latach 2018-2022')
    plt.bar(index, k_2018, width, color='gold', label='Rok_2018')
    plt.bar(index + 1, k_2019, width, color='black', label='Rok_2019')
    plt.bar(index + 2, k_2020, width, label='Rok_2020')
    plt.bar(index + 3, k_2021, width, label='Rok_2021')
    plt.xticks(ticks=range(4), labels=lab2, rotation=70)
    plt.legend()
    # plt.show()
    plt.savefig('./static/img/003')

    # In[562]:

    fig, a = plt.subplots(2, 2, figsize=(8, 7))
    explode = (0, 0.1)
    colors = ['#ff6666', '#99ff99']
    # ,'#99ff99','#ffcc99','#ff9999','#66b3ff'
    langs = ['Kobiet', 'Mężczyzn']
    # plt.title('Populacja mężczyzn w stosunku do kobiet w roku 2018')
    dane_21 = [k_2021, m_2021]
    dane_20 = [k_2020, m_2020]
    dane_19 = [k_2019, m_2019]
    dane_18 = [k_2018, m_2018]

    a[0][0].pie(dane_21, labels=langs
                , autopct='%1.2f%%'
                , shadow=True
                , explode=explode
                , colors=colors)
    a[0][0].set_title('Podział według płci rok 2021')
    a[0][1].pie(dane_20, labels=langs
                , autopct='%1.2f%%'
                , shadow=True
                , explode=explode
                , colors=colors)
    a[0][1].set_title('Podział według płci rok 2020')
    a[1][0].pie(dane_19, labels=langs
                , autopct='%1.2f%%'
                , shadow=True
                , explode=explode
                , colors=colors)
    a[1][0].set_title('Podział według płci rok 2019')
    a[1][1].pie(dane_18, labels=langs
                , autopct='%1.2f%%'
                , shadow=True
                , explode=explode
                , colors=colors)
    a[1][1].set_title('Podział według płci rok 2018')
    # plt.show()
    plt.savefig('./static/img/004')

    # In[563]:

    MAX_21 = df[df["ogółem_2021"] == df['ogółem_2021'].max()]
    MIN_21 = df[df["ogółem_2021"] == df['ogółem_2021'].min()]
    AVG_21 = df[df["ogółem_2021"] > df['ogółem_2021'].mean()]
    _MAX_21 = MAX_21['ogółem_2021']
    _MAX_name_21 = MAX_21['Nazwa']
    _MIN_21 = MIN_21['ogółem_2021']
    _MIN_name_21 = MIN_21['Nazwa']
    _AVG_21 = AVG_21['ogółem_2021']
    _AVG_name_21 = AVG_21['Nazwa']

    figure(figsize=(13, 6), dpi=72)
    # plt.yticks(np.arange(0, 40, 1))

    lab3 = [[_MAX_name_21], [_MIN_name_21]]
    width = 0.5
    index = 0
    plt.title('Województwo o największej i najmniejszej populacji w roku 2021')
    plt.bar(index, _MAX_21, width, color='purple', label='Największe zaludnienie')
    plt.bar(index + 1, _MIN_21, width, color='orange', label='Najmniejsze zaludnienie')
    plt.xticks(ticks=range(2), labels=lab3, rotation=0)
    plt.legend()
    # plt.show()
    plt.savefig('./static/img/005')

    # In[564]:

    lab4 = AVG_21['Nazwa']
    v1 = AVG_21['ogółem_2018']
    v2 = AVG_21['ogółem_2019']
    v3 = AVG_21['ogółem_2020']
    v4 = AVG_21['ogółem_2021']

    figure(figsize=(13, 6), dpi=72)
    width = 0.16
    index = np.arange(len(lab4))
    plt.title('Województwa z liczbą mieszkańców powyżej średnie w latach 2018-2021')
    plt.bar(index - 0.25, v1, width, color='#66b3ff', label='Rok_2018')
    plt.bar(index - 0.09, v2, width, color='#ff9999', label='Rok_2019')
    plt.bar(index + 0.08, v3, width, color='#ffcc99', label='Rok_2020')
    plt.bar(index + 0.25, v4, width, color='#99ff99', label='Rok_2021')
    plt.xticks(ticks=range(6), labels=lab4, rotation=70)
    plt.legend()
    # plt.show()
    plt.savefig('./static/img/006')

#Wynagrodzenie
    df_wyn = pd.read_csv('./static/WYNA.csv', sep=';', decimal=',')
    df_wyn.drop(df_wyn.columns[[0, 6]], axis=1, inplace=True)
    # df_wyn.drop(0, axis=0, inplace=True)
    df_wyn.rename(columns={'rok;ogółem;2018;[zł]': 'ogółem_2018'
        , 'rok;ogółem;2019;[zł]': 'ogółem_2019'
        , 'rok;ogółem;2020;[zł]': 'ogółem_2020'
        , 'rok;ogółem;2021;[zł]': 'ogółem_2021'
                           }, inplace=True)

    fig, ax = plt.subplots(figsize=(8, 8))
    # pl=df_wyn.loc[df_wyn["Nazwa"] == "POLSKA","ogółem_2021"]
    value = df_wyn['ogółem_2021'].values.tolist()
    name = df_wyn['Nazwa'].values.tolist()
    avg = np.mean(value)
    plt.style.use('tableau-colorblind10')
    ax.set(xlabel='Wynagrodzenie brutto', ylabel='Województwa',
           title='Przeciętne miesięczne wynagrodzenia brutto w roku 2021')

    ax.barh(name, value)
    ax.axvline(avg, ls='--', color='r')
    # plt.show()
    plt.savefig('./static/img/wynagrodzenie.png')

# #Bezrobocie
#     df = pd.read_csv('./static/RYNE.csv', sep=';', decimal=',')
#
#     df.head(8)
#     # N1=N.copy()
#
#     df.dtypes
#
#     df.drop(df.columns[[0, 10]], axis=1, inplace=True)
#
#     # In[481]:
#
#     df.rename(columns={'ogółem;2018;[%]': 'ogółem_2018_[%]'
#         , 'ogółem;2019;[%]': 'ogółem_2019_[%]'
#         , 'ogółem;2020;[%]': 'ogółem_2020_[%]'
#         , 'ogółem;2021;[%]': 'ogółem_2021_[%]'}, inplace=True)
#
#     df1 = df.copy()
#     df.drop(0, axis=0, inplace=True)
#
#     values1 = df['ogółem_2018_[%]']
#     values2 = df['ogółem_2019_[%]']
#     values3 = df['ogółem_2020_[%]']
#     values4 = df['ogółem_2021_[%]']
#     lab = df['Nazwa']
#     figure(figsize=(15, 6), dpi=70)
#     width = 0.16
#     index = np.arange(len(lab))
#     plt.title('Stopień bezrobocia w województwach w latach 2018-2021')
#     plt.bar(index - 0.25, values1, width, color='#33ff00', label='Rok_2018')
#     plt.bar(index - 0.09, values2, width, color='#6600ff', label='Rok_2019')
#     plt.bar(index + 0.08, values3, width, color='#9933cc', label='Rok_2020')
#     plt.bar(index + 0.25, values4, width, label='Rok_2021')
#     plt.xticks(ticks=range(16), labels=lab, rotation=50)
#     plt.legend()
#     # plt.show()
#     # plt.savefig('./static/img/bezrobocie01.png')
#
#     df1 = df1.head(1)
#
#     values5 = df1['ogółem_2018_[%]']
#     values6 = df1['ogółem_2019_[%]']
#     values7 = df1['ogółem_2020_[%]']
#     values8 = df1['ogółem_2021_[%]']
#     lab2 = df1['Nazwa']
#     figure(figsize=(8, 6), dpi=70)
#     width = 0.05
#     index = np.arange(len(lab2))
#     plt.title('Stopień bezrobocia w Polsce w latach 2018-2021')
#     plt.bar(index - 0.25, values5, width, color='#33ff00', label='Rok_2018')
#     plt.bar(index - 0.08, values6, width, color='#6600ff', label='Rok_2019')
#     plt.bar(index + 0.09, values7, width, color='#9933cc', label='Rok_2020')
#     plt.bar(index + 0.25, values8, width, label='Rok_2021')
#     plt.xticks(ticks=range(1), labels=lab2, rotation=0)
#     plt.legend()
#
#     df = df.head(15)
#
#     MAX_19 = df[df["ogółem_2019_[%]"] == df['ogółem_2019_[%]'].max()]
#     MIN_19 = df[df["ogółem_2019_[%]"] == df['ogółem_2019_[%]'].min()]
#     AVG_19 = df[df["ogółem_2019_[%]"] > df['ogółem_2019_[%]'].mean()]
#
#     _MAX_name_19 = MAX_19['Nazwa'].to_string()
#     _MIN_name_19 = MIN_19['Nazwa'].to_string()
#     _AVG_name_19 = AVG_19['Nazwa'].to_string()
#
#     figure(figsize=(4, 3), dpi=70)
#
#     lab2 = [_MIN_name_19, _MAX_name_19]
#     width = 0.1
#     index = 0
#     plt.title('Stopień bezrobocia min/max przy podziale na województwa w roku 2019')
#     plt.bar(index, _MIN_19, width, color='#339933', label='Najmniejsze bezrobocie %')
#     plt.bar(index + 1, _MAX_19, width, color='Yellow', label='Największe bezrobocie %')
#     plt.xticks(ticks=range(2), labels=lab2, rotation=0)
#     plt.legend()
#     # plt.show()
#     plt.savefig('./static/img/bezrobocie02.png')
#======================================Service End=======================================

    return render_template('index.html', msg=msg)


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pythonlogin.accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO pythonlogin.accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/data_table - this will be the page with data table
@app.route('/data_table')
def data_table():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('data_table.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/chart')
def chart():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('chart.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pythonlogin.accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
