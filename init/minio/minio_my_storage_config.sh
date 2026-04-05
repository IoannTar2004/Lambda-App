mc alias set myminio http://minio-my-storage:9000 $MINIO_MY_ROOT_USER $MINIO_MY_ROOT_PASSWORD

mc admin config set myminio notify_webhook:1 endpoint="http://events-service:8002/api/events/publish/s3" \
auth_token=$COMMUNICATION_TOKEN

mc admin service restart myminio --json