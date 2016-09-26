#!/usr/bin/python

#Features TODO: we could run cygwin shell script to check if current branch is master
#and switch to master if not. Dont remember to run git stash before that.

import os
import subprocess
import shutil
import time
from time import sleep
from subprocess import Popen
from time import gmtime, strftime

CVSCmd = "cvs"

# TODO: tag needs to be updated when new build comes
CVSTag = "REL_11_0_0_BRANCH "

#############################################################################################
#
#       Step 1. Sync latest source files from CVS for both cvsroot and snap driver
#
#############################################################################################

# CVS login token
CVSLoginToken = ":pserver:kgao:Chang40zhe@ncvs.commvault.com:/cvs/cvsrepro/GX"
# option to override CVSROOT env variable, see http://docstore.mik.ua/orelly/other/cvs/cvs-CHP-10-SECT-1.htm
CVSOptionLogin = " -d " + CVSLoginToken + " login"

# Force clear flag
CVSForceClean = " -C "

cmd = CVSCmd + CVSOptionLogin 
#res = Popen(cmd)
print("Now logging into cvs...")
subprocess.call(cmd)

# Sleep 20s since sometimes login is pretty slow
#print("Now wait for 20s until logon is OK")
#sleep(20)

# run cygwin script to change current branch to master before synchronize
# we will call git stash if current branch is not master
shellCmd = 'd:/cygwin64/bin/bash --login -c "sh /home/kgao/chkgit.sh"'
subprocess.call(shellCmd)

#snapDrive = 'd:/snapDrives/'
# May need change when a new snap folder is generated
#curSnapFolder = 'v11B80/'
cvsRoot = 'd:/cvsroot/'
cteLibPath = "c:/V11/"

# Code locations that I might need to change
# TODO: we might also add new folders
codeLocation = [
"CTE", 
"CTEJava",
"CTELibraries"
]

codeLocationEx = [
"CTELibraries"
]

def syncCVS(targetFolder, codePath):
	for x in codePath:
	# update local cvs folder first
		curDir = targetFolder + x
		#print curDir
		os.chdir(curDir)
		newcmd = CVSCmd + " update -P -C -d -r " + CVSTag
		print newcmd
		# res = Popen(newcmd)
		subprocess.call(newcmd)
	print("Synchronize [" + targetFolder +"] from CVS is done...:)");

# Step 1. Sync CVS code to local CVS folder. This should be quick
syncCVS(cvsRoot, codeLocation)

print("Step 1: CVS synchronize on local cvsroot is done... :)")

syncCVS(cteLibPath, codeLocationEx);

print("Step 2: CVS synchronize on local CTELibrary is done... :)")

print("Completed... :)");

