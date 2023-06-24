import secrets
import sqlite3
from flask import Flask, request, make_response, render_template

app = Flask(__name__)
db_file = 'sessions.db'

# Connect to the SQLite database
def connect_to_database():
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print("Error connecting to the database: ", e)
        return None
    
# Create the sessions table if it doesn't already exist
def create_sessions_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_id INTEGER,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                expired_at TIMESTAMP
            )
        ''')
        connection.commit()
    except sqlite3.Error as e:
        print("Error creating the sessions table: ", e)

@app.route('/')
def home():
    # Check if the client has a session cookie
    if 'session_cookie' in request.cookies:
        session_cookie = request.cookies.get('session_cookie')

        # Validate the session cookie
        if validate_cookie(session_cookie, connect_to_database()):
            # Get the session details from the database
            connection = connect_to_database()
            if connection is None:
                return 'Error connecting to the database'
            
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (session_cookie,))
            session = cursor.fetchone()

            # Extract the session details
            session_id = session[1]
            expires_at = session[5]

            # Render the home page with the session details
            return render_template('home.html', logged_in=True, session_id=session_id, expires_at=expires_at)
        
    # If no session cookie found, render the home page without the session details
    return render_template('home.html', logged_in=False)

@app.route('/login')
def login():
    # Connect to the database
    connection = connect_to_database()
    if connection is None:
        return 'Error connecting to the database'
    
    # Create the sessions table if it doesn't already exist
    create_sessions_table(connection)

    # Check to see if the client already has a session
    if 'session_cookie' in request.cookies:
        valid_cookie = validate_cookie(request.cookies.get('session_cookie'), connection)
        if valid_cookie:
            return 'You already have a session cookie! <br>Your session ID is: ' + valid_cookie[1] + '. <br>Your session expires at: ' + valid_cookie[5] + '.'

    # If no valid cookie found, generate a new cookie
    session_cookie = generate_cookie()

    # Store the cookie in the database
    store_cookie(connection, session_cookie)

    # Close the database connection
    connection.close()

    # Set the cookie in the client
    response = make_response("You have been logged in!")
    response.set_cookie('session_cookie', session_cookie)

    return response
        
@app.route('/logout')
def logout():
    # Connect to the database
    connection = connect_to_database()
    if connection is None:
        return 'Error connecting to the database'
    
    # Check if the client has a session cookie
    if 'session_cookie' in request.cookies:
        session_cookie = request.cookies.get('session_cookie')

        # Delete the session cookie from the database
        try:
            cursor = connection.cursor()
            cursor.execute('''
                DELETE FROM sessions WHERE session_id = ?
            ''', (session_cookie,))
            connection.commit()
        except sqlite3.Error as e:
            print("Error deleting the session cookie from the database: ", e)

        # Close the database connection
        connection.close()

        # Delete the session cookie from the client
        response = make_response('You have been logged out!')
        response.set_cookie('session_cookie', '', expires=0)

        return response


def validate_cookie(session_cookie, connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT * FROM sessions WHERE session_id = ? AND expired_at > datetime('now')
        ''', (session_cookie,))
        result = cursor.fetchone()

        # Check if the cookie exists and is not expired
        if result is not None:
            return result

        return False
    except sqlite3.Error as e:
        print("Error validating the session cookie: ", e)
        return False

def generate_cookie():
    # Generate a random hex string
    return secrets.token_hex(16)

def store_cookie(connection, session_cookie):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO sessions (session_id, created_at, updated_at, expired_at)
            VALUES (?, datetime('now'), datetime('now'), datetime('now', '+30 minutes'))
        ''', (session_cookie,))
        connection.commit()
    except sqlite3.Error as e:
        print("Error storing the session in the database: ", e)