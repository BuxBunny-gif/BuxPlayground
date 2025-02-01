from flask import Flask, request, render_template, redirect
import sqlite3
import os


#template_dir = os.path.abspath('webFiles\\templates')

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "webFiles", "templates"))
print(app.template_folder)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sql_injection', methods=['GET', 'POST'])
def sql_injection():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()

    result = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # ⚠️ Unsicher! Direkte SQL-Abfrage mit String-Manipulation
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        try:
            cur.execute(query)
            user = cur.fetchone()
        except sqlite3.OperationalError:
            user = None
        
        
        
        if user:
            result = f"✅ Login erfolgreich! Willkommen, {user[1]}."
        else:
            result = "❌ Falscher Benutzername oder Passwort."
    
    return render_template('sql_injection.html', result=result)

@app.route('/user_count_xss', methods=['GET', 'POST'])
def user_count_xss():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Benutzeranzahl abrufen
    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]

    # Eine unsichere "Kommentare"-Tabelle erstellen (für XSS)
    cur.execute("CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, comment TEXT)")
    conn.commit()

    last_comment = ""

    if request.method == 'POST':
        comment = request.form['comment']

        # ⚠️ UNSICHER: Speichert die Eingabe ohne Filterung -> Ermöglicht XSS
        cur.execute("INSERT INTO comments (comment) VALUES (?)", (comment,))
        conn.commit()

        # Den letzten Kommentar abrufen
        cur.execute("SELECT comment FROM comments ORDER BY id DESC LIMIT 1")
        last_comment = cur.fetchone()[0]

    conn.close()
    
    return render_template('xss.html', user_count=user_count, last_comment=last_comment)

@app.route('/reset_db', methods=['POST'])
def reset_db():
    """Setzt die Datenbank zurück (löscht alle Benutzer & Kommentare)."""
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM comments")
    cur.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'comments'") 
    conn.commit()
    conn.close()
    return redirect('/user_count_xss')



if __name__ == '__main__':
    app.run(debug=True)