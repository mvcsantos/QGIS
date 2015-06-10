import sys

from PyQt4.QtCore import QSettings, QCoreApplication, QObject, pyqtSlot, pyqtSignal
from processing.core.ProcessingLog import ProcessingLog
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.tools import dataobjects
from processing.tools.system import getTempFilename
from processing.tools import vector
from processing.gui.SilentProgress import SilentProgress

# processing.runalg('qgis:creategrid', 0, "0,1,0,1", 0.1, 0.1, "EPSG:4326", None)

class AlgorithmExecutor(QObject):

    #started = QtCore.pyqtSignal()
    #process = QtCore.pyqtSignal(int)
    #stop = QtCore.pyqtSignal()
    setResult= pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, alg, progress = None, parent = None):
        QObject.__init__(self, parent)
        self.alg = alg
        self.progress = progress
        self.result = True

    def runalg(self):
        """Executes a given algorithm, showing its progress in the
        progress object passed along.

        Return true if everything went OK, false if the algorithm
        could not be completed.
        """
        if self.progress is None:
            self.progress = SilentProgress()
        try:
            self.alg.execute(self.progress)
            
            self.setResult.emit()
        except Exception, e:
            ProcessingLog.addToLog(sys.exc_info()[0], ProcessingLog.LOG_ERROR)
            self.progress.error(e.msg)
            self.setResult.emit()
            print e
            self.result = False

    def runalgIterating():
        pass

    def tr(self, string, context=''):
        if context == '':
            context = 'AlgorithmExecutor'
        return QCoreApplication.translate(context, string)
