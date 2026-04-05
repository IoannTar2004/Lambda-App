mc alias set myminio http://minio-code:9000 $MINIO_CODE_ROOT_USER $MINIO_CODE_ROOT_PASSWORD

mc mb myminio/user-code --ignore-existing
mc mb myminio/code-archives --ignore-existing
mc mb myminio/function-logs --ignore-existing
