# -*- coding: utf-8 -*-

"""
***************************************************************************
    SagaUtils.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import stat
import subprocess

from PyQt4.QtCore import QCoreApplication, QObject
from qgis.core import QgsApplication
from processing.core.ProcessingConfig import ProcessingConfig
from processing.core.ProcessingLog import ProcessingLog
from processing.tools.system import isWindows, isMac, userFolder



class SagaUtils(QObject):
    
    SAGA_LOG_COMMANDS = 'SAGA_LOG_COMMANDS'
    SAGA_LOG_CONSOLE = 'SAGA_LOG_CONSOLE'
    SAGA_FOLDER = 'SAGA_FOLDER'
    SAGA_IMPORT_EXPORT_OPTIMIZATION = 'SAGA_IMPORT_EXPORT_OPTIMIZATION'
    _installedVersion = None
    _installedVersionFound = False
    
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        

    def sagaBatchJobFilename(self):
        if isWindows():
            filename = 'saga_batch_job.bat'
        else:
            filename = 'saga_batch_job.sh'
    
        batchfile = userFolder() + os.sep + filename
    
        return batchfile
    
    
    def findSagaFolder(self):
        folder = None
        if isMac():
            testfolder = os.path.join(QgsApplication.prefixPath(), 'bin')
            if os.path.exists(os.path.join(testfolder, 'saga_cmd')):
                folder = testfolder
            else:
                testfolder = '/usr/local/bin'
                if os.path.exists(os.path.join(testfolder, 'saga_cmd')):
                    folder = testfolder
        elif isWindows():
            testfolder = os.path.join(os.path.dirname(QgsApplication.prefixPath()), 'saga')
            if os.path.exists(os.path.join(testfolder, 'saga_cmd.exe')):
                folder = testfolder
        return folder
    
    def sagaPath(self):
        folder = ProcessingConfig.getSetting(SagaUtils.SAGA_FOLDER)
        if folder is None or folder == '':
            folder = self.findSagaFolder()
            if folder is not None:
                ProcessingConfig.setSettingValue(SagaUtils.SAGA_FOLDER, folder)
        return folder or ''
    
    def sagaDescriptionPath(self):
        return os.path.join(os.path.dirname(__file__), 'description')
    
    
    def createSagaBatchJobFileFromSagaCommands(self, commands):
    
        fout = open(self.sagaBatchJobFilename(), 'w')
        if isWindows():
            fout.write('set SAGA=' + self.sagaPath() + '\n')
            fout.write('set SAGA_MLB=' + self.sagaPath() + os.sep
                       + 'modules' + '\n')
            fout.write('PATH=PATH;%SAGA%;%SAGA_MLB%\n')
        elif isMac():
            fout.write('export SAGA_MLB=' + self.sagaPath()
                       + '/../lib/saga\n')
            fout.write('export PATH=' + self.sagaPath() + ':$PATH\n')
        else:
            pass
        for command in commands:
            fout.write('saga_cmd ' + command.encode('utf8') + '\n')
    
        fout.write('exit')
        fout.close()
    
    def getSagaInstalledVersion(self,runSaga=False):
        if not SagaUtils._installedVersionFound or runSaga:
            if isWindows():
                commands = [os.path.join(self.sagaPath(), "saga_cmd.exe"), "-v"]
            elif isMac():
                commands = [os.path.join(self.sagaPath(), "saga_cmd"), "-v"]
            else:
                commands = ["saga_cmd", "-v"]
            proc = subprocess.Popen(
                commands,
                shell=True,
                stdout=subprocess.PIPE,
                stdin=open(os.devnull),
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            ).stdout
            try:
                lines = proc.readlines()
            except:
                return None
            for line in lines:
                if line.startswith("SAGA Version:"):
                    SagaUtils._installedVersion = line[len("SAGA Version:"):].strip().split(" ")[0]
            SagaUtils._installedVersionFound = True
        return SagaUtils._installedVersion
    
    def executeSaga(self):
        if isWindows():
            command = ['cmd.exe', '/C ', self.sagaBatchJobFilename()]
        else:
            os.chmod(self.sagaBatchJobFilename(), stat.S_IEXEC
                     | stat.S_IREAD | stat.S_IWRITE)
            command = [self.sagaBatchJobFilename()]
        loglines = []
        loglines.append(QCoreApplication.translate('SagaUtils', 'SAGA execution console output'))
        proc = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=open(os.devnull),
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        ).stdout
        try:
            for line in iter(proc.readline, ''):
                if '%' in line:
                    s = ''.join([x for x in line if x.isdigit()])
                    try:
                        self.parent().progress.emit(int(s))
                    except:
                        pass
                else:
                    line = line.strip()
                    if line != '/' and line != '-' and line != '\\' and line != '|':
                        loglines.append(line)
                        self.parent().setConsoleInfo.emit(line)
        except:
            pass
        if ProcessingConfig.getSetting(SagaUtils.SAGA_LOG_CONSOLE):
            ProcessingLog.addToLog(ProcessingLog.LOG_INFO, loglines)
