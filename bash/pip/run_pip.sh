#!/bin/bash
requirment_filename="./src/requirements.txt" #
source_filename="requirements_versions.txt"

dst_filename="./requirements_with_versions.txt"

# get all installed packages  from $dst_filename if it does not exist
if [ ! -f $source_filename ]; then
	eval "$($(which conda) 'shell.bash' 'hook')"
	echo && echo " -> Saving the installed pip packages to the file:"
	echo  " - filepath = $source_filename"
	## freeze the installed  packages 
	echo && echo "please wait while the seach is ongoing..."
	pip freeze > requirements_versions.txt
else
echo && echo " -> The installed pip packages will be loaded from the file:"
echo  " - filepath = $source_filename"
fi

## delete old output requirements file
if [ -f $dst_filename ]; then
	rm $dst_filename
	echo && echo " -> the previous output file is removed from:"
	echo " - filepath = $dst_filename "
fi

# create empty output requirements file
touch  $dst_filename

## filter the requested packages with the installed versions 
while read -r line; do
		if [[ $line != '' && $line != *"#"* && $line != *"-e"* ]]; then
			if [[ $line == *"=="* || $line == *"<="* || $line == *">="* ]];then
				# get the installed <package_name>
				package_name=$(sed 's/>=/==/g' <<< "$line")
				package_name=$(sed 's/<=/==/g' <<< "$package_name")
				IFS='==' read -r -a array <<< "$package_name"
				package_name="${array[0]}"
			else
				package_name=$line
			fi

			# remove the unlisted packages <package_name>
			sed "/${package_name}/!d" requirements_versions.txt  >> $dst_filename
		fi

		# keep the comments lines
		if [[ $line != '' && $line == *"#"* ]]; then
			# !TODO-bug: keep commented packages without new line
			# echo && echo "package_name=$package_name"
			# echo "line=$line"
			echo ""  >> $dst_filename
			echo "$line"  >> $dst_filename
		fi


done < "$requirment_filename"

##  add the package setup line
# echo '##### package setup' >> $dst_filename
echo '-e .' >> $dst_filename
# rm requirements_versions.txt

##----------------------------------------------------------------
#  show the output file
# clear
# cat $dst_filename
echo && echo " -> the new output file with packages with versions is saved in:"
echo " - filepath = $dst_filename "
