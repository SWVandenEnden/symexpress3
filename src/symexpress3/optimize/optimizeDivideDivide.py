#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (C) 2026 Gien van den Enden - swvandenenden@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from symexpress3          import symexpress3
from symexpress3.optimize import optimizeBase

class OptimizeDivideDivide( optimizeBase.OptimizeBase ):
  """
  Divide divide = normal
  \n 1 / 1 / x become x
  """
  def __init__( self ):
    super().__init__()
    self._name         = "divideDivide"
    self._symtype      = "*"
    self._desc         = "Divide divide is normal, 1/1/x = x"


  def optimize( self, symExpr, action ):
    result = False

    if self.checkExpression( symExpr, action ) != True:
      return result

    # only 1 / (x * y)  accepted
    if (# symExpr.powerCounter     >  1 or
        symExpr.powerSign       != -1 or
        # symExpr.powerDenominator >  1 or
        symExpr.onlyOneRoot     !=  1 or
        symExpr.numElements()    <  2
      ) :
      return result

    # search if there is a 1/x item
    lFound = False
    for elem in symExpr.elements :
      if elem.powerSign == -1:
        lFound = True
        break
    if lFound == False:
      return result

    # at least 1 1/x exist so make 2 list
    elemUpper = symexpress3.SymExpress( '*',  1, 1,  1 )
    elemDown  = symexpress3.SymExpress( '*', -1, 1 , 1 )

    result = True

    for elem in symExpr.elements :
      if elem.powerSign == -1:
        elem.powerSign = 1
        elemUpper.elements.append( elem )
      else:
        elemDown.elements.append( elem )

    symExpr.powerSign = 1
    symExpr.elements = []
    symExpr.elements.append( elemUpper )
    symExpr.elements.append( elemDown  )

    return result

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check( testClass, symOrg, symTest, wanted ):
    if display == True :
      print( f"naam      : {testClass.name}" )
      print( f"orginal   : {str( symOrg  )}" )
      print( f"optimized : {str( symTest )}" )

    if str( symTest ).strip() != wanted:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}' )

  result = False
  symTest = symexpress3.SymFormulaParser( '1 / ( a * (1/pi) * (1/e) )' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  symOrg = symTest.copy()

  testClass = OptimizeDivideDivide()
  result |= testClass.optimize( symTest, "divideDivide" )

  _Check( testClass, symOrg, symTest, "pi * e * (a)^^-1" )


if __name__ == '__main__':
  Test( True )
