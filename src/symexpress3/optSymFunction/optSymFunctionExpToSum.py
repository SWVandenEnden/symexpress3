#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Sym Express 3

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

    https://en.wikipedia.org/wiki/Exponential_function

"""
import typing

from symexpress3 import symexpress3
from symexpress3 import optFunctionBase
from symexpress3 import symtools

class OptSymFunctionExpToSum( optFunctionBase.OptFunctionBase ):
  """
  Convert exp into a sum
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "expToSum"
    self._desc         = "Convert exp into a sum"
    self._funcName     = "exp"                    # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 2                        # maximum number of parameters


  def optimize( self, elem:symexpress3.TypVarSym3Object, action:None|str ) -> None|symexpress3.TypVarSym3Object:

    if self.checkType( elem, action ) != True:
      return None

    elem = typing.cast( symexpress3.SymFunction, elem )

    elemParam = elem.elements[ 0 ]

    if elem.numElements() > 1:
      elemPar2 = elem.elements[ 1 ]
      elemPar1 = symexpress3.SymExpress( '*' )

      elemLog = symexpress3.SymFunction( 'log' )
      elemLog.add( elemPar2 )

      elemPar1.add( elemParam )
      elemPar1.add( elemLog   )

      elemParam = elemPar1

    elemSum = symexpress3.SymFunction( 'sum' )

    varName = symtools.VariableGenerateGet()
    elemVar = symexpress3.SymVariable( varName )

    elemSum.add( elemVar )
    elemSum.add( symexpress3.SymNumber( 1,0,1 )       ) # zero
    elemSum.add( symexpress3.SymVariable( 'infinity') )

    elemFunc = symexpress3.SymExpress( '*' )

    elemPower = symexpress3.SymFunction( 'exp' )
    elemPower.add( elemVar   )
    elemPower.add( elemParam )

    elemFunc.add( elemPower )

    elemFact = symexpress3.SymFunction( 'factorial')
    elemFact.add( elemVar )
    elemFact.powerSign = -1

    elemFunc.add( elemFact )

    elemSum.add( elemFunc )

    elemSum.powerCounter     = elem.powerCounter
    elemSum.powerDenominator = elem.powerDenominator
    elemSum.powerSign        = elem.powerSign
    elemSum.onlyOneRoot      = elem.onlyOneRoot

    return elemSum

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """

  def _Check( testClass:OptSymFunctionExpToSum
            , symOrg   :symexpress3.TypVarSym3Object
            , symTest  :None|symexpress3.TypVarSym3Object
            , wanted   :str
            ) -> None :
    if display == True :
      print( f"naam      : {testClass.name}" )
      print( f"orginal   : {str( symOrg  )}" )
      print( f"optimized : {str( symTest )}" )

    if str( symTest ).strip() != wanted:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'SymFunction optimize {testClass.name}, unit test error: {str( symTest )}, expected: {wanted}, value: {str( symOrg )}' )

  symtools.VariableGenerateReset()

  symTest:symexpress3.TypVarSym3Object = symexpress3.SymFormulaParser( "exp( 3 )" )
  symTest.optimize()
  symTest = typing.cast( symexpress3.SymFunction, symTest )
  symTest = symTest.elements[ 0 ]

  testClass = OptSymFunctionExpToSum()
  symNew    = testClass.optimize( symTest, "expToSum" )

  _Check( testClass, symTest, symNew, "sum( n1,0,infinity, exp( n1,3 ) *  factorial( n1 )^^-1 )" )


  symtools.VariableGenerateReset()

  symTest = symexpress3.SymFormulaParser( "exp( x, 3 )" )
  symTest.optimize()
  symTest = typing.cast( symexpress3.SymFunction, symTest )
  symTest = symTest.elements[ 0 ]

  testClass = OptSymFunctionExpToSum()
  symNew    = testClass.optimize( symTest, "expToSum" )

  _Check( testClass, symTest, symNew, "sum( n1,0,infinity, exp( n1,x *  log( 3 ) ) *  factorial( n1 )^^-1 )" )

if __name__ == '__main__':
  Test( True )
