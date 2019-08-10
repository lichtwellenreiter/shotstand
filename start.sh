source simpleappenv/bin/activate
gunicorn --workers 5 --bind unix:simpleapp.sock -m 007 src:app
deactivate