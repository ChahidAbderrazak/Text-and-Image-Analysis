# mount the dvc remote
clear
new_data=data/test/
tagname="dvc1"
message='add testing data: csv, json. jpg, xlsx'

#### ------------  DVC LIST OF REMOTE STORAGES -------------
echo && echo " -[DVC] List of the dvc remote storages "
dvc remote list

#### ------------  DEFINE THE DEFAULT REMOTE STORAGE -------------
echo && echo " -[dvc] define the DVC remote storage  "
dvc remote default $DVC_REMOTE_STORAGE

#### ------------  TAG/PUSH DATA CHANGES -------------
echo && echo " -[git] tag the current version and push the changes "
git tag -a $tagname -m "${message}"
dvc add $new_data
dvc push