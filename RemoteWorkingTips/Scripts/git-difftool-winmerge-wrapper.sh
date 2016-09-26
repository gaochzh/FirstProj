#!/bin/sh
echo "Launching WinMergeU.exe \"$(cygpath -aw "$1")\" \"$(cygpath -aw "$2")\""
if [ -f $1 -a -f $2 ]
then
  "C:/Program Files (x86)/WinMerge/WinMergeU.exe" -e -u -wl -dl "Base" -dr "Mine" "$(cygpath -aw "$1")" "$(cygpath -aw "$2")"
else
  echo "skipping as one file doesn't exist"
fi
