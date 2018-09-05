#!/bin/bash
#
# Copyright 2018 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if [ "$#" -ne 1 ]; then
  echo "usage: deploy-webapp.sh prod|test|public|local"
  exit 1
fi

if [ $1 = "public" ]; then
  SERVICE="vtslab-schedule"
elif [ $1 = "local" ]; then
  dev_appserver.py ./
  exit 0
else
  SERVICE="vtslab-schedule-$1"
fi

echo "Fetching endpoints service version of $SERVICE ..."
ENDPOINTS=$(gcloud endpoints configs list --service=$SERVICE.appspot.com)
arr=($ENDPOINTS)

if [ ${#arr[@]} -lt 4 ]; then
  echo "You need to deploy endpoints first."
  exit 0
else
  VERSION=${arr[2]}
  NAME=${arr[3]}
  echo "ENDPOINTS_SERVICE_NAME: $NAME"
  echo "ENDPOINTS_SERVICE_VERSION: $VERSION"
fi

echo "Updating app.yaml ..."
if [ "$(uname)" == "Darwin" ]; then
  sed -i "" "s/ENDPOINTS_SERVICE_NAME:.*/ENDPOINTS_SERVICE_NAME: $NAME/g" app.yaml
  sed -i "" "s/ENDPOINTS_SERVICE_VERSION:.*/ENDPOINTS_SERVICE_VERSION: $VERSION/g" app.yaml
else
  sed -i "s/ENDPOINTS_SERVICE_NAME:.*/ENDPOINTS_SERVICE_NAME: $NAME/g" app.yaml
  sed -i "s/ENDPOINTS_SERVICE_VERSION:.*/ENDPOINTS_SERVICE_VERSION: $VERSION/g" app.yaml
fi

echo "Deploying the web app to $SERVICE ..."

gcloud app deploy app.yaml cron.yaml index.yaml queue.yaml worker.yaml --project=$SERVICE

echo "Deployment done!"
