
from processing.gui.AlgorithmExecutor import AlgorithmExecutor
from processing.core.ProcessingLog import ProcessingLog
from processing.core.CancelledAlgorithmExecutionException import CancelledAlgorithmExecutionException
from PyQt4.QtCore import QRunnable

class AlgorithmExecutorTask(QRunnable):
    
    
    def __init__(self, algExecutor = None):
        super(AlgorithmExecutorTask, self).__init__()
        self.algExecutor = algExecutor
     
     
    def run(self):
        if self.algExecutor is None:
            raise Exception("Algorithm Executor is None")
        try:
            if self.algExecutor.paramToIter:
                self.algExecutor.runalgIterating()
            else:
                command = self.algExecutor.alg.getAsCommand()
                if command:
                    ProcessingLog.addToLog(ProcessingLog.LOG_ALGORITHM, command)
                self.algExecutor.runalg()
        except CancelledAlgorithmExecutionException, e:
            ProcessingLog.addToLog(ProcessingLog.LOG_INFO, "Algorithm Execution Cancelled...")
            self.algExecutor.setResult.emit(False)
            self.algExecutor.alg.executionCancelled = False
        except Exception as e:
            print "AlgorithmExecutor Taks"
            print e
            ProcessingLog.addToLog(ProcessingLog.LOG_ERROR, e)
            self.algExecutor.setResult.emit(False)