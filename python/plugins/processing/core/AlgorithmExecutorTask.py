
from processing.gui.AlgorithmExecutor import AlgorithmExecutor
from processing.core.ProcessingLog import ProcessingLog
from PyQt4.QtCore import QRunnable

class AlgorithmExecutorTask(QRunnable):
    
    
    def __init__(self, alg, iterateParam):
        super(AlgorithmExecutorTask, self).__init__()
        self.algExecutor = AlgorithmExecutor(alg)
        self.iterateParam = iterateParam
     
     
    def run(self):
        if self.iterateParam:
            self.algExecutor.runalgIterating()
        else:
            
            command = self.algExecutor.alg.getAsCommand()
            if command:
                ProcessingLog.addToLog(ProcessingLog.LOG_ALGORITHM, command)
            
            self.algExecutor.runalg()
            