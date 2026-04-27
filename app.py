from flask import Flask, request, redirect, url_for, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'secretkey'

DATABASE = 'hw13.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect('/dashboard')
        else:
            return "Invalid login"
    return '''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit">
        </form>
    '''

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/login')
    return "Dashboard (we will build more here)"
@app.route('/student/<int:student_id>')
def student_results(student_id):
    if not session.get('logged_in'):
        return redirect('/login')

    db = get_db()
    results = db.execute(
        "SELECT quiz_id, score FROM results WHERE student_id = ?",
        (student_id,)
    ).fetchall()

    if not results:
        return "<h1>No Results</h1><br><a href='/dashboard'>Back</a>"

    return f"""
    <h1>Student Results</h1>
    {results}
    <br><br>
    <a href='/dashboard'>Back</a>
    """
if __name__ == '__main__':
    app.run(debug=True)
