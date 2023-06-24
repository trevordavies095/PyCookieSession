# PyCookieSession

PyCookieSession is a Python project that implements a simple cookie session management system using Flask. It consists of a client-side application and a server-side application that communicate over HTTP.

## Overview

The PyCookieSession project aims to provide a cookie-based session management solution. The server application serves a cookie to the client if one is not present, or validates the given cookie to maintain an active session. The server stores session information in an SQLite database.

## Features

- Cookie-based session management
- Server-side session validation and expiration
- SQLite database for session storage

## Technologies Used

- Python
- Flask
- SQLite

## Setup

1. Clone the repository:
`git clone https://github.com/trevordavies095/PyCookieSession.git`

2. Navigate to the project directory: `cd PyCookieSession`

3. Install the required dependencies: `pip install -r requirements.txt`

4. Start the Flask server: `flask run`

5. Open a web browser and visit [http://localhost:5000](http://localhost:5000) to access the client application.

## Usage

- To initiate a session, access the `/login` route. If a valid session cookie is present, the server will display the session information. Otherwise, a new session cookie will be generated.

- To log out and end the session, access the `/logout` route.

- Accessing the `/` route will display the session status and session ID if a valid session is active.

## Contributing

Contributions to PyCookieSession are welcome! If you find any issues or have suggestions for improvements, please feel free to submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).