#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Cos to sum for Sym Express 3

    Copyright (C) 2024 Gien van den Enden - swvandenenden@gmail.com

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

from symexpress3 import symexpress3
from symexpress3 import optFunctionBase

class OptSymFunctionCosToSum( optFunctionBase.OptFunctionBase ):
  """
  Convert cos to sum
  """
  def __init__( self ):
    super().__init__()
    self._name         = "cosToSum"
    self._desc         = "Convert cos to sum"
    self._funcName     = "cos"                    # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 1                        # maximum number of parameters


  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    elemParam = elem.elements[ 0 ]

    # https://en.wikipedia.org/wiki/Trigonometric_functions
    elemSym = symexpress3.SymFormulaParser( "sum( n, 0 ,20, exp( n, -1 ) * exp( 2 * n, x ) / factorial( 2 * n ) )" )

    dDict = {}
    dDict[ 'x' ] = str( elemParam )

    elemSym.replaceVariable( dDict )

    elemSym.powerCounter     = elem.powerCounter
    elemSym.powerDenominator = elem.powerDenominator
    elemSym.powerSign        = elem.powerSign
    elemSym.onlyOneRoot      = elem.onlyOneRoot

    return elemSym

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest = symexpress3.SymFormulaParser( "cos(pi/4)" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  # print( "symTest: " + str( symTest ))

  testClass = OptSymFunctionCosToSum()
  symNew    = testClass.optimize( symTest, "cosToSum" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "sum( n,0,20, exp( n,(-1) ) *  exp( 2 * n,pi * 1 * 4^^-1 ) *  factorial( 2 * n )^^-1 )":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymFunction optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )

if __name__ == '__main__':
  Test( True )
