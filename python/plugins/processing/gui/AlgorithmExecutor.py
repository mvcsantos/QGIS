import sys

from qgis.core import QgsFeature, QgsVectorFileWriter
from PyQt4.QtCore import QSettings, QCoreApplication, QObject, pyqtSlot, pyqtSignal
from processing.core.ProcessingLog import ProcessingLog
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.gui.Postprocessing import handleAlgorithmResults
from processing.tools import dataobjects
from processing.tools.system import getTempFilename
from processing.tools import vector
from processing.gui.SilentProgress import SilentProgress
import time

# processing.runalg('qgis:creategrid', 0, "0,1,0,1", 0.1, 0.1, "EPSG:4326", None)

class AlgorithmExecutor(QObject):

    setResult = pyqtSignal(bool)
    finished = pyqtSignal()

    setPercentage = pyqtSignal(int)
    setText = pyqtSignal(str)

    def __init__(self, alg, parent = None):
        QObject.__init__(self, parent)
        self.alg = alg
        self.paramToIter = None

    def runalg(self):
        """Executes a given algorithm, showing its progress in the
        progress object passed along.

        Return true if everything went OK, false if the algorithm
        could not be completed.
        """
        try:
            self.alg.execute()
            self.setResult.emit(True)
        except Exception as e:
            ProcessingLog.addToLog(sys.exc_info()[0], ProcessingLog.LOG_ERROR)
            print e
            self.finished.emit()

    def runalgIterating(self):
         # Generate all single-feature layers
        settings = QSettings()
        systemEncoding = settings.value('/UI/encoding', 'System')
        layerfile = self.alg.getParameterValue(self.paramToIter)
        layer = dataobjects.getObjectFromUri(layerfile, False)
        feat = QgsFeature()
        filelist = []
        outputs = {}
        provider = layer.dataProvider()
        features = vector.features(layer)
        for feat in features:
            output = getTempFilename('shp')
            filelist.append(output)
            writer = QgsVectorFileWriter(output, systemEncoding,
                    provider.fields(), provider.geometryType(), layer.crs())
            writer.addFeature(feat)
            del writer
     
        # store output values to use them later as basenames for all outputs
        for out in self.alg.outputs:
            outputs[out.name] = out.value
    
        # now run all the algorithms
        for i,f in enumerate(filelist):
            self.alg.setParameterValue(self.paramToIter, f)
            for out in self.alg.outputs:
                filename = outputs[out.name]
                if filename:
                    filename = filename[:filename.rfind('.')] + '_' + str(i) \
                        + filename[filename.rfind('.'):]
                out.value = filename
            self.setText.emit(self.tr('Executing iteration %s/%s...' % (str(i), str(len(filelist)))))
            self.setPercentage.emit(i * 100 / len(filelist))
            # TODO: figure out how to solve this problem
            # because the runalg doesn't return anything 
            if self.runalg():
                handleAlgorithmResults(self.alg, None, False)
            else:
                self.setResult.emit(False)
    
        self.setResult.emit(True)
        
    def tr(self, string, context=''):
        if context == '':
            context = 'AlgorithmExecutor'
        return QCoreApplication.translate(context, string)
