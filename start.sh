source shotvenv/bin/activate
gunicorn --workers 3 --bind unix:shotstand.sock  -m 007 app:app
deactivate
