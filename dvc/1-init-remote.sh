# mount the dvc remote
clear
#### ------------  INITIALIZATIONy -------------
# pip install dvc dvc[s3]
dvc init
S3_ENDPOINT_URL=s3://dvcstore # please make sure the bucket is already created

#### ------------  LOCAL directoty -------------
# echo && echo " -[local] mounting the dvc remote storage "
# dvc remote add -d dvcstore  /media/abdo2020/DATA/database/dvcstore_local
echo && echo " -[DVC] List of the dvc remote storages "
dvc remote list
# #### ------------  LOCAL S3 Minio -------------
. .env  # load .env variable: passwords,  AWS S3 credentials
. .env-ip
. .env-ip-mlops


if [ "${MINIO_SERVER_URL}" != "" && "${DVC_REMOTE_STORAGE}" != "" ]; then
	dvc remote add -d $DVC_REMOTE_STORAGE $S3_ENDPOINT_URL -f
	
	#  add MinIO credentials (from .env variables)
	dvc remote modify minio endpointurl $MINIO_SERVER_URL
	dvc remote modify minio access_key_id $MINIO_ACCESS_KEY
	dvc remote modify minio secret_access_key $MINIO_SECRET_KEY

else

echo && echo "Error: one or more variable are not found in .env: " && echo 
echo "- MINIO_SERVER_URL=${MINIO_SERVER_URL}"
echo "- DVC_REMOTE_STORAGE=${DVC_REMOTE_STORAGE}"

fi