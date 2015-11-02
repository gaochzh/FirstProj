#!/bin/sh

fileListName='/cygdrive/d/cvsroot/filesToCopy.txt'

echo "The following files will be copied to snap driver:"
printf "\n"

mapfile -t fileNames < <(git diff --name-only)

printf "%s\n" "${fileNames[@]}"

set -- ${fileNames[*]}
if [ $# -eq 0 ] ; then

echo "Nothing to copy..."

else

printf "\n"
echo 'Please press Y to confirm, others to quit:'
read kbInput

if [ $kbInput = 'Y' ] || [ $kbInput = 'y' ]
then

snapRoot='/cygdrive/d/snapDrives/v11B80/'

for (( i=0; i<${#fileNames[@]}; i++ )); do 
#   echo ${fileNames[i]} >> $fileListName
   echo "Now copy ${fileNames[i]} to $snapRoot${fileNames[i]}"
   cp -f ${fileNames[i]} "$snapRoot${fileNames[i]}";
done

printf "\n"
echo "Finish copy files to snap folder..."

else

echo "Now quit..."
fi

fi
