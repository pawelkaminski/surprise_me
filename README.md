# surprise_me

### frontend

### backend

create virtualenv:

```bash
virtualenv -p /usr/bin/python3.7 venv 
. venv/bin/activate
pip install -r backend/requirements.txt
```

we need mongodb v 4.2

at docker

```bash
sudo docker run mongo:4.2
```

or install it as a service


please copy settings_example.py and create own settings.py

then import databases
```bash
python import_dbs.py
```


to run flask:

```bash
export FLASK_APP=run.py
flask run
```

or to run gunicorn from surprise_me directory level

```bash
gunicorn -w 1 --bind 0.0.0.0:8000 backend.run:application
```
