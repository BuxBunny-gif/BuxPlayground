from flask import Flask, request, render_template
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
        cur.execute(query)
        user = cur.fetchone()
        
        if user:
            result = f"✅ Login erfolgreich! Willkommen, {user[1]}."
        else:
            result = "❌ Falscher Benutzername oder Passwort."
    
    return render_template('sql_injection.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)