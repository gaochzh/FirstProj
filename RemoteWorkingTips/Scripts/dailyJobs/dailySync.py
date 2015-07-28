#!/usr/bin/python

#Features TODO: we could run cygwin shell script to check if current branch is master
#and switch to master if not. Dont remember to run git stash before that.

import os
import subprocess
import shutil
import time
from time import sleep
from subprocess import Popen

CVSCmd = "cvs"

# TODO: tag needs to be updated when new build comes
CVSTag = "REL_11_0_0_BRANCH "

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

snapDrive = 'd:/snapDrives/'
# May need change when a new snap folder is generated
curSnapFolder = 'v11B80/'
cvsRoot = 'd:/cvsroot/'

# Code locations that I might need to change
# TODO: we might also add new folders
codeLocation = [
"vaultcx/Source/Include", 
"vaultcx/Source/CommServer/CVInstallManagerDBInterface", 
"vaultcx/Source/CommServer/CVInstallManager",
"vaultcx/Source/CommServer/Db",
"vaultcx/Source/CommServer/CVPatchesUpdateDBServer",
"vaultcx/Source/CommServer/CVUpdates",
"vaultcx/Source/CommServer/FtpPatchDownload",
"vaultcx/Source/CommServer/ScheduledPatchesUpdate",
"vaultcx/Source/CommServer/startPrePostCmd",
"vaultcx/Source/CommServer/AppMgr",
"vaultcx/Source/CommServer/EvAppMgr",

"vaultcx/Source/Common/CVInstallClient",
"vaultcx/Source/Common/CVInstallCommon",
"vaultcx/Source/Common/CVInstallNetwork",
"vaultcx/Source/Common/CvInternetGateway",
"vaultcx/Source/Common/CvNameChange",
"vaultcx/Source/Common/CvPatchesCommon",
"vaultcx/Source/Common/CvPatchesUpdateDBClient",
"vaultcx/Source/Common/SIMCallWrapper",
"vaultcx/Source/Common/CvSim",
"vaultcx/Source/Common/CvUnixSetup",

"vaultcxtools/DatabaseUpgrade/CommServer",
"vaultcxtools/SetPreImagedNames"
]

for x in codeLocation:
# update local cvs folder first
	curDir = cvsRoot + x
#	print curDir
	os.chdir(curDir)
	newcmd = CVSCmd + " update -P -r " + CVSTag
#	print newcmd
# 	res = Popen(newcmd)
	subprocess.call(newcmd)

#timeInterval = 120
# Sleep some time before syncing the other one
#sleep(timeInterval)

for x in codeLocation:
# update local cvs folder first
	curDir = snapDrive + curSnapFolder + x
	print curDir
	os.chdir(curDir)
	newcmd = CVSCmd + " update -P -r " + CVSTag
	print newcmd
	# res = Popen(newcmd)
	subprocess.call(newcmd)

#sleep(timeInterval)

print("CVS synchronize on both local and snap folder is done... :)")