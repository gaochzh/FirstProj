#!/bin/sh

cd /cygdrive/d/cvsroot

branch_name=$(git symbolic-ref -q HEAD)

echo "Current branch is $branch_name"

if [ $branch_name = 'refs/heads/master' ]
then
   echo 'Current branch is already master...';
else
   git stash;
   git checkout master;
   echo 'Switched to branch master before sync...'
fi
