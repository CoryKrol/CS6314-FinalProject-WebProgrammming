## How to run
### PyCharm
1. Go to edit configurations
2. Add new Flask Server configuration
3. Settings
   - `Target type: Script path`
   - `Target: <path_to_hedgehog.py>`
   - `FLASK_ENV: [development|testing|production]` 

### From command line
To run set the FLASK_APP environment variable
```
$ export FLASK_APP=hedgehog.py
$ export FLASK_DEBUT=1
$ flask run
 * Serving Flask app "hedgehog.py" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```