#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Asin function for Sym Express 3

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


    https://en.wikipedia.org/wiki/Inverse_trigonometric_functions
"""

import typing
import mpmath # type:ignore

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncTrigonoBase

class SymFuncAsin( symFuncTrigonoBase.SymFuncTrigonoBase ):
  """
  Asin function
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name      = "asin"
    self._desc      = "asin"
    self._minparams = 1    # minimum number of parameters
    self._maxparams = 1    # maximum number of parameters
    self._syntax    = "asin(<x>)"


  def functionToValue( self, elem:None|symexpress3.TypVarSym3Object ) -> None|symexpress3.TypVarSym3Object :

    if self._checkCorrectFunction( elem ) != True:
      return None

    elem = typing.cast( symexpress3.SymFunction, elem )

    result = self._conversTableToArc( elem )
    if result != None:
      return result

    result = self._convertSinCosTanAtanSign( elem )
    if result != None:
      return result

    return None


  def _getValueSingle( self, dValue:symexpress3.TypVarSym3Value, dValue2:None|symexpress3.TypVarSym3Value = None ) -> symexpress3.TypVarSym3Value :
    return mpmath.asin( dValue )



#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """
  def _Check( testClass :SymFuncAsin
            , symTest   :symexpress3.TypVarSym3Object
            , value     :None|symexpress3.TypVarSym3Object
            , dValue    :symexpress3.TypVarSym3Value
            , valueCalc :str
            , dValueCalc:symexpress3.TypVarSym3Value
            ) -> None :

    dValue = symexpress3.SymRound( dValue, 10 )

    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ) != valueCalc or dValue != dValueCalc:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value}' )

  symTest = symexpress3.SymFormulaParser( 'asin( 1 )' )
  symTest.optimize()
  testClass = SymFuncAsin()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "1 * 2^^-1 * pi", round( 1.5707963268, 10) )


  symTest = symexpress3.SymFormulaParser( 'asin( -1 )' )
  symTest.optimize()
  testClass = SymFuncAsin()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "(-1) *  asin( 1 )", round( -1.5707963268, 10) )


if __name__ == '__main__':
  Test( True )
