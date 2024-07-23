#!/bin/bash
gnome-terminal -- bash -c "cd libra-vue-frontend;npm run dev;"
gnome-terminal -- bash -c "cd libra-flask-backend/; python3 app.py"
gnome-terminal -- bash -c "cd libra-flask-backend/;celery -A app.celery beat --loglevel=info"
gnome-terminal -- bash -c "cd libra-flask-backend/;celery -A app.celery worker -l info -E"