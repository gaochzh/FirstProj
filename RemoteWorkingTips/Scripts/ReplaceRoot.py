#!/usr/bin/python

import os
import subprocess
import shutil
from subprocess import Popen

# This script is used to replace all pbuilder with kgao when creating a new snap driver
# However we still need to manually change the folder security option to grant kgao full control on those folders

snapDrive = 'd:/snapDrives/'
# May need change when a new snap folder is generated
curSnapFolder = 'v11B80/'

curRoot = snapDrive + curSnapFolder
repBatName = "ReplaceRoot.bat"
repBatPath = curRoot + "vaultcx/"
repBatFileLoc = repBatPath + repBatName
#print repBatFileLoc

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

"vaultcx/Source/Common/CvLib",
"vaultcx/Source/Common/CvDataPipe",
"vaultcx/Source/Common/EventMessage",
"vaultcx/Source/Common/XmlMessage",

"vaultcx/Source/Installer/Source/Common/Include",
"vaultcx/Source/Installer/Source/RemoteInstall",

"vaultcxtools/DatabaseUpgrade/CommServer",
"vaultcxtools/SetPreImagedNames"
]

for x in codeLocation:
#	print curRoot + x
	curDir = curRoot + x;
#	print curDir
	os.chdir(curDir)
	shutil.copy(repBatFileLoc, curDir)
	newcmd = repBatFileLoc + ' kgao'
	subprocess.call(newcmd)