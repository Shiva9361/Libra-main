#!/bin/bash
gnome-terminal -- bash -c "cd frontend/Libra-v2;npm run dev;"
gnome-terminal -- bash -c "cd backend/; python3 app.py"
gnome-terminal -- bash -c "cd backend;celery -A app.celery beat --loglevel=info"
gnome-terminal -- bash -c "cd backend;celery -A app.celery worker -l info -E"