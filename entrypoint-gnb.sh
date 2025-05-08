#!/bin/bash
echo "Waiting for AMF..."
while ! nc -uz ${AMF_ADDR} 2152; do sleep 1; done
envsubst < gnb_config.template.yml > config.yml
env
cat config.yml
exec gnb -c config.yml
