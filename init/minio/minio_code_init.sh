mc alias set myminio http://minio-code:9000 $MINIO_CODE_ROOT_USER $MINIO_CODE_ROOT_PASSWORD
sleep 5

mc mb myminio/user-code
mc mb myminio/code-archives
mc mb myminio/function-logs
