from flask import Flask, render_template, flash, request, redirect, url_for, session
import flask_bootstrap
import flask
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
flask_bootstrap.Bootstrap(app)

# Configure DB
db = yaml.full_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

# Pocetna stranica i prikaz u slucaju greske
@app.route ('/')
def index():
    if session.get('username') is None:
        return render_template('login.html')
    else:
        return render_template('pocetna.html')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



# Registracija, Prijava i Odjava

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        username = request.form.get('username')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password_confirm = request.form.get('passwordConfirm')
        if password == password_confirm:
            if (cur.execute("SELECT * from User where username = %s", [username]) == 0) and len(username) >= 4:
                if cur.execute("SELECT * from User where email = %s", [email]) == 0:
                    cur.execute("INSERT INTO User(firstname,lastname,email,password,username) VALUES (%s,%s,%s,%s,%s)",
                                [firstname, lastname, email, password, username])
                    mysql.connection.commit()
                    cur.close()
                    flash('Регистрација је успјешна!', 'success')
                    return redirect(url_for('login'))
                else:
                    flash('Наведена мејл адреса је заузета!', 'danger')
                    return render_template("registration.html")
            else:
                flash('Корисничко име је заузето!', 'danger')
                return render_template("registration.html")
        else:
            flash('Лозинка се не поклапа!', 'danger')
            return render_template("registration.html")
    return render_template("registration.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))  # Korisnik je već prijavljen, preusmeri ga na početnu stranicu

    if request.method == 'POST':
        cur = mysql.connection.cursor()
        username = request.form.get('username')
        password = request.form.get('password')

        if cur.execute("SELECT * from User WHERE username = %s AND password = %s", (username, password)) > 0:
            user = cur.fetchone()

            # Čuvanje više informacija o korisniku u sesiji
            session['login'] = True
            session['username'] = user[6]
            session['firstName'] = user[4]
            session['lastName'] = user[5]
            session['admin'] = user[7]

            # Ažuriranje polja 'active' u tabeli User na 1
            cur.execute("UPDATE User SET active = 1 WHERE username = %s", [username])
            mysql.connection.commit()

            return redirect(url_for('index'))
        else:
            flask.flash('Погрешан корисник или шифра!', 'danger')
            return render_template('login.html')
    else:
        return render_template('login.html')


# Odjava korisnika
@app.route('/logout')
def logout():
    if session.get('username') is not None:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE User SET active = 0 WHERE username = %s ", [session['username']])
        mysql.connection.commit()
        session.pop('username')
        return redirect(url_for("login"))
    else:
        return render_template("login.html")



# Kartica Geodete
    # Prikaz tabele geodete iz baze podataka
@app.route('/geodete')
def prikaz():
    if session.get('username') is None:
        return render_template('login.html')
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from Registar_Geodeta")
        geodet = cur.fetchall()
        return render_template("prikaz_geodeta.html", podaci=geodet)

    # Dodavanje novog geodete
@app.route ('/geodet', methods=['GET', 'POST'])
def geodet():
    if session.get('username') is None:
        return render_template('login.html')
    else:
        if session.get('username') is not None and session.get('admin') == 1:
            if request.method == 'POST':
                ime = request.form['name']
                prezime = request.form['lastname']
                jmbg = request.form['jmbg']
                strucna_sprema = request.form['ssprema']
                broj_strucnog = request.form['brstrucnog']
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO Registar_Geodeta (JMBG,Ime,Prezime,Strucna_Sprema,Broj_Strucnog) VALUES (%s,%s,%s,%s,%s)",
                                        [jmbg, ime, prezime, strucna_sprema, broj_strucnog])
                mysql.connection.commit()
                flash('Додали сте геодету у базу геодета!', 'success')
                return redirect(url_for('prikaz'))                
            else:
                return render_template("geodete.html")
        else:
            flash('Само администратор може да врши унос података!!!', 'danger')
            return redirect(url_for('prikaz'))


    # Pristupanje profilu jednog geodete na osnovu njegovog ID-a
@app.route ('/geodet/<int:id>')
def geo(id):
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * from Registar_Geodeta WHERE ID = %s", [id])
    if result_value > 0:
        g=cur.fetchone()
        return render_template("geodet.html", geod=g)
    return render_template("prikaz_geodeta.html")

    # Brisanje geodete na osnovu njegovog ID-a
@app.route ('/brisi/<int:id>')
def brisi(id):
    if session.get('username') is None:
        return render_template('login.html')
    else:
        if session.get('username') is not None and session.get('admin') == 1:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM Registar_Geodeta WHERE ID = %s", [id])
            mysql.connection.commit()
            flash('Геодета је обрисан!', 'success')
            return redirect(url_for('prikaz'))
    flash('Само администратор може извршити брисање!', 'success')
    return redirect(url_for('prikaz'))

    # Uredjivanje podataka unutar baze za jednog geodetu
@app.route ('/uredi', methods=['POST', 'GET'])
def uredi():
    if session.get('username') is None:
        return render_template('login.html')
    else:
        if session.get('username') is not None and session.get('admin') == 1:
            if request.method == 'POST':
                id=request.form['id']
                ime = request.form['name']
                prezime = request.form['lastname']
                jmbg = request.form['jmbg']
                strucna_sprema = request.form['ssprema']
                broj_strucnog = request.form['brstrucnog']
                cur = mysql.connection.cursor()
                cur.execute("""
                            UPDATE Registar_Geodeta
                            SET JMBG=%s, Ime=%s, Prezime=%s, Strucna_Sprema=%s, Broj_Strucnog=%s
                            WHERE ID = %s
                            """, [jmbg, ime, prezime, strucna_sprema, broj_strucnog, id])
                flash('Успјешно те измјенили податке!', 'success')
                mysql.connection.commit()
                return redirect(url_for('prikaz'))           
            else:
                return render_template("prikaz_geodeta.html")
        else:
            flash('Само администратор може да врши уређивање података!!!', 'danger')
            return redirect(url_for('prikaz'))


# Kartica Organizacije
    # Prikaz tabele firmi iz baze podataka
@app.route ('/organizacije')
def organizacije():
    if session.get('username') is None:
        return render_template('login.html')
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from Registar_Firmi")
        organizacije = cur.fetchall()
        return render_template("prikaz_firmi.html", firme=organizacije)
    
    # Dodavanje nove firme
@app.route ('/organizacija', methods=['GET', 'POST'])
def firma():
    if session.get('username') is None:
        return render_template('login.html')
    else:
        if session.get('username') is not None and session.get('admin') == 1:
            if request.method == 'POST':
                naziv_firme = request.form['nfirme']
                adresa = request.form['ulica'] +' бр. ' + request.form['broj'] +', ' + request.form['grad']
                jib = request.form['jib']
                telefon = request.form['tel']
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO Registar_Firmi (JIB,Naziv,Adresa,Broj_Telefona) VALUES (%s,%s,%s,%s)",
                                        [jib, naziv_firme, adresa, telefon])
                mysql.connection.commit()
                flash('Додали сте геодетску фирму у базу геодетских организација!', 'success')
                return redirect(url_for('organizacije'))                
            else:
                return render_template("dodavanje_firmi.html")
        else:
            flash('Само администратор може да врши унос података!!!', 'danger')
            return redirect(url_for('organizacije'))


# Kartica Instrumenti
    # Prikaz tabele instrumenata iz baze podataka
@app.route('/instrumenti')
def instrumenti():
    if session.get('username') is None:
        return render_template('login.html')
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from Registar_Instrumenata")
        instrumenti = cur.fetchall()
        return render_template("prikaz_instrumenata.html", inst=instrumenti)

    # Dodavanje novоg instrumenta
@app.route ('/instrument', methods=['GET', 'POST'])
def instrument():
    if session.get('username') is None:
        return render_template('login.html')
    else:
        if session.get('username') is not None and session.get('admin') == 1:
            if request.method == 'POST':
                tip_isntrumenta = request.form['tip_inst']
                proizvodjac = request.form['proizvodjac']
                seriski_broj = request.form['serbroj']
                datum = request.form['datum']
                vlasnik = request.form['vlasnik']
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO Registar_Instrumenata (Seriski_broj,Tip_Instrumenta,Proizvodjac,Etaloniran_DO,Registar_Firmi_JIB) VALUES (%s,%s,%s,%s,%s)",
                                        [seriski_broj, tip_isntrumenta, proizvodjac, datum, vlasnik])
                mysql.connection.commit()
                flash('Додали сте иснтрумент у базу геодетских инструмената!', 'success')
                return redirect(url_for('instrumenti'))                
            else:
                return render_template("dodavanje_instrumenta.html")
        else:
            flash('Само администратор може да врши унос података!!!', 'danger')
            return redirect(url_for('instrumenti'))



if __name__ == "__main__":
    app.run(debug=True)