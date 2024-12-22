# please install <mc> using : https://min.io/docs/minio/linux/reference/minio-mc.html#quickstart

##---------------------  LOAD VARIABLES --------------------------

. .env  # load .env variable: passwords,  AWS S3 credentials
. .env-ip
. .env-ip-mlops

##---------------------  ADD the ALIAS --------------------------
#   add an alias for a MinIO deployment:
#  - name : myminio running at the URL MINIO_SERVER_URL
mc alias set myminio $MINIO_SERVER_URL $MINIO_ACCESS_KEY $MINIO_SECRET_KEY