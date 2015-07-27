# -*- coding: utf-8 -*-

"""
***************************************************************************
    CancelledAlgorithmExecutionException.py
    ---------------------
    Date                 : July 2015
    Copyright            : (C) 2015 by Marcus Santos
    Email                : mvcs at me dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Marcus Santos'
__date__ = 'July 2015'
__copyright__ = '(C) 2015, Marcus Santos'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

class CancelledAlgorithmExecutionException(Exception):
	
	def __init__(self, msg='Cancelled Algorithm Execution'):
		super(CancelledAlgorithmExecutionException, self).__init__(msg)