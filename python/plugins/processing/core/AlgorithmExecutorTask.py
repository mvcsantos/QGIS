
from processing.gui.AlgorithmExecutor import AlgorithmExecutor
from PyQt4.QtCore import QRunnable

class AlgorithmExecutorTask(QRunnable):
    
    
    def __init__(self, alg):
        super(AlgorithmExecutorTask, self).__init__()
        self.algExecutor = AlgorithmExecutor(alg)
     
     
    def run(self):
        self.algExecutor.runalg()
        