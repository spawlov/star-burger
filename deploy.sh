#!/bin/bash
set -e
echo
echo "Starting deploy..."
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
echo "Updating Node.js packages..."
npm ci
npm audit fix
echo "Node.js packages updated."
echo "=================================================================="
echo "Rebuilding frontend..."
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
echo "Frontend rebuild."
echo "=================================================================="
echo "Rebuilding staticfiles..."
python manage.py collectstatic --noinput
echo "Staticfiles rebuild."
echo "=================================================================="
echo "Migrations are applied..."
python manage.py migrate --noinput
echo "Migrations completed."
echo "=================================================================="
echo "Restarting Gunicorn..."
systemctl restart starburger
echo "Restart Gunicorn completed."
echo "=================================================================="
echo "Reloading Nginx..."
systemctl reload nginx
echo "Nginx reloaded"
echo "=================================================================="
set +e && ROLLBAR_TOKEN=$(grep "ROLLBAR_TOKEN" .env) && set -e
ROLLBAR_ACCESS_TOKEN=${ROLLBAR_TOKEN##*"="}
if [[ -z $ROLLBAR_ACCESS_TOKEN ]];
then
  echo "ROLLBAR_TOKEN not set"
else
  GIT_SHA=$(git rev-parse HEAD)
  ENVIRONMENT=production
  curl https://api.rollbar.com/api/1/deploy/ \
      --form access_token="$ROLLBAR_ACCESS_TOKEN" \
      --form environment=$ENVIRONMENT \
      --form revision="$GIT_SHA" \
      --form local_username="$USER" \
      --form status=succeeded | jq -r '.data.deploy_id'
  echo "=================================================================="
fi
chmod g+x deploy.sh
echo "Deploy completed."
