## Requirements
1. Flask-Mail: used for sending auth emails
2. Flask-Boostrap: Seamless integration of Bootstrap libraries in flask templates
3. Flask-WTF: Plugin to extend and simplify web form backend
4. Flask-Login: Manages sessions of logged-in users
5. Werkzeug: password hashing and verification
6. itsdangerous: Cryptographic token generation and verification
## How to run
### Run application
#### PyCharm
1. Go to edit configurations
2. Add new Flask Server configuration
3. Settings
   - `Target type: Script path`
   - `Target: <path_to_hedgehog.py>`
   - `FLASK_ENV: [development|testing|production]` 

#### From command line
To run set the FLASK_APP environment variable
Set the FLASK_CONFIG environment variable to switch environments
```
$ export FLASK_APP=hedgehog.py
$ export FLASK_DEBUT=1
$ export FLASK_CONFIG=development
$ flask run
 * Serving Flask app "hedgehog.py" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
### Run Unit Tests
`$ flask test`

### Run DB Migration Scripts
This project uses the Flask-Migrate plugin to generate and applies alembic scripts for automatic database migration
#### Initialize migration folder
Should not need to be run
`$ flask db init`
#### Create new migration scripts after model changes
`$ flask db migration -m "<message>"`
#### Apply migration scripts to database
`$ flask db migration upgrade`