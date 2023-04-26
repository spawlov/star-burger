#!/bin/bash
set -e
echo
echo "Starting deploy..."
echo "=================================================================="
cd /opt/StarBurger
echo "Directory changed to "$PWD
echo "=================================================================="
echo "Pull from repository..."
git pull
echo "Pull from repository completed."
echo "=================================================================="
echo "Activating venv..."
source venv/bin/activate
echo "Venv activated."
echo "=================================================================="
echo "Updating requirements..."
pip install -r requirements.txt
echo "Requirements updated."
echo "=================================================================="
echo "Updating Node.js packges..."
npm update
npm audit fix
echo "Node.js packages updated."
echo "=================================================================="
echo "Rebuilding frontend..."
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
echo "Frontend rebuilded."
echo "=================================================================="
echo "Rebuiding staticfiles..."
python manage.py collectstatic --noinput
echo "Staticfiles rebuilded."
echo "=================================================================="
echo "Migrations are applied..."
python manage.py migrate
echo "Migrations completed."
echo "=================================================================="
echo "Restarting Gunicorn..."
systemctl restart starburger
echo "Restart Gunicorn copleted."
echo "=================================================================="
echo "Reloading Nginx..."
systemctl reload nginx
echo "Nginx reloaded"
echo "=================================================================="
GIT_SHA=`git rev-parse HEAD`
ROLLBAR_ACCESS_TOKEN=0df9740359ad4ce5ab85b6da18972849
ENVIRONMENT=production
curl https://api.rollbar.com/api/1/deploy/ \
    --form access_token=$ROLLBAR_ACCESS_TOKEN \
    --form environment=$ENVIRONMENT \
    --form revision=$GIT_SHA \
    --form local_username=$USER \
    --form status=succeeded #| jq -r '.data.deploy_id'
echo "=================================================================="
chmod g+x deploy.sh
echo "Deploy completed."
