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

snapDrive = 'd:/snapDrives/'
# May need change when a new snap folder is generated
curSnapFolder = 'v11B80/'
cvsRoot = 'd:/cvsroot/'

# Code locations that I might need to change
# TODO: we might also add new folders
codeLocation = [
"vaultcx/Source/Include", 
"vaultcx/Source/CommServer/CVInstallManagerDBInterface"  #, 
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

"vaultcx/Source/Common/CvLib",
"vaultcx/Source/Common/CvDataPipe",
"vaultcx/Source/Common/EventMessage",
"vaultcx/Source/Common/XmlMessage",
"vaultcx/Source/Common/clusterUtils",

"vaultcx/Source/Installer/Source/Common/Include",
"vaultcx/Source/Installer/Source/RemoteInstall",

"vaultcxtools/DatabaseUpgrade/CommServer",
"vaultcxtools/SetPreImagedNames",
"vaultcxtools/CopyToCacheDLL"
]

def syncCVS(targetFolder):
	for x in codeLocation:
	# update local cvs folder first
		curDir = targetFolder + x
		#print curDir
		os.chdir(curDir)
		newcmd = CVSCmd + " update -P -r " + CVSTag
		print newcmd
		# res = Popen(newcmd)
		subprocess.call(newcmd)
	print("Synchronize [" + targetFolder +"] from CVS is done...:)");

# Step 1. Sync CVS code to local CVS folder. This should be quick
syncCVS(cvsRoot)

print("Step 1: CVS synchronize on local is done... :)")

# Step 2. Create a thread to sync CVS folder on snap driver. This could be slow depends on network speed
from threading import Thread
from time import sleep

thread = Thread(target = syncCVS, args = (snapDrive + curSnapFolder, ))
thread.start()
print "A new thread has been created to sync snap folder."

#sleep(timeInterval)

# Build include projects in local. This should run simontaneously with snap CVS sync
############################################################################################################
#
#       Step 3. Use MsBuild to automatically build XMLMessage, EventMessage, DB_Include and DB_SQL project
#
############################################################################################################

curDateTime = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
logSuffix = "_" + curDateTime + ".log"
buildLogPrefix = "D:\\dailyJobs\\Logs\\buildLog_"
errorLogPrefix = "D:\\dailyJobs\\Logs\\errorLog_"

# We could add more projects using msbuild here
# , ["DB_SQL", "D:\\cvsroot\\vaultcx\\Source\\Project\\winnt40_intel\\..\\..\\CommServer\\Db\\DB_SQL.vcxproj"]
buildProjects = [
["XMLMessage", "D:\\cvsroot\\vaultcx\\Source\\Project\\winnt40_intel\\CvXMLMsgs\\XMLMessage.vcxproj"]
, ["EventMessage", "D:\\cvsroot\\vaultcx\\Source\\Project\\winnt40_intel\\..\\..\\Common\\EventMessage\\Include\\EventMessage.vcxproj"]
, ["DB_Include", "D:\\cvsroot\\vaultcx\\Source\\Project\\winnt40_intel\\..\\..\\CommServer\\Db\\Include\\DB_Include.vcxproj"]
]

msbuildCmd1 = "C:\\Program Files (x86)\\MSBuild\\12.0\\Bin\\amd64\\msbuild.exe  -t:clean;rebuild -p:Configuration=Release;Platform=x64 -p:BuildProjectReferences=false /FileLogger /FileLogger2 /fileLoggerParameters:LogFile="
msbuildCmd2 = ";;verbosity=normal /FileLoggerParameters2:LogFile="
msbuildCmd3 = ";errorsonly /noconsolelogger /verbosity:normal "

for x in buildProjects:
	buildLog = buildLogPrefix + x[0] + logSuffix
	print buildLog
	errorLog = errorLogPrefix + x[0] + logSuffix
	print errorLog
	curbuildCmd = msbuildCmd1 + buildLog + msbuildCmd2 + errorLog + msbuildCmd3 + x[1]
	print curbuildCmd
	subprocess.call(curbuildCmd)

print("Step 3: MsBuild on autogen projects is done... :)")

thread.join();

print("After join, step 2: sync code on snap drive is done... :)");

