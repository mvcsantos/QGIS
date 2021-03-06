# -*- coding: utf-8 -*-

"""
***************************************************************************
    general.py
    ---------------------
    Date                 : April 2013
    Copyright            : (C) 2013 by Victor Olaya
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
__date__ = 'April 2013'
__copyright__ = '(C) 2013, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from processing.core.Processing import Processing
from processing.gui.Postprocessing import handleAlgorithmResults
from processing.core.parameters import ParameterSelection
from PyQt4.QtCore import QThreadPool

# Dedicated threadPool to run the algorithms 
processingThreadPool = QThreadPool()
processingThreadPool.expiryTimeout()
processingThreadPool.setExpiryTimeout(30*1000)

algResults = {}
processing = Processing(processingThreadPool)

def alglist(text=None):
    s = ''
    for provider in Processing.algs.values():
        sortedlist = sorted(provider.values(), key=lambda alg: alg.name)
        for alg in sortedlist:
            if text is None or text.lower() in alg.name.lower():
                s += alg.name.ljust(50, '-') + '--->' + alg.commandLineName() \
                    + '\n'
    print s


def algoptions(name):
    alg = Processing.getAlgorithm(name)
    if alg is not None:
        s = ''
        for param in alg.parameters:
            if isinstance(param, ParameterSelection):
                s += param.name + '(' + param.description + ')\n'
                i = 0
                for option in param.options:
                    s += '\t' + str(i) + ' - ' + str(option) + '\n'
                    i += 1
        print s
    else:
        print 'Algorithm not found'


def alghelp(name):
    alg = Processing.getAlgorithm(name)
    
    if alg is not None:
        alg = alg.getCopy()
        print str(alg)
        algoptions(name)
    else:
        print 'Algorithm not found'


def runalg(algOrName, *args):
    global processing
    processing = Processing(processingThreadPool)
    processing.setAlgorithmResult.connect(storeAlgResult)
    processing.runAlgorithm(algOrName, None, *args)
    #if alg is not None:
    #    return alg.getOutputValuesAsDictionary()


def runandload(name, *args):
    global processing
    processing = Processing(processingThreadPool)
    processing.setAlgorithmResult.connect(storeAlgResult)
    processing.runAlgorithm(name, handleAlgorithmResults, *args)


def storeAlgResult(result):
    global algResults
    algResults.update({'OUTPUT'+str(len(algResults)):result.values()[0]})
    print result
    
def getThreadPool():
    return processingThreadPool
    