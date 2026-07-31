#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Gcd function voor Sym Express 3

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


    https://en.wikipedia.org/wiki/Greatest_common_divisor

"""
import typing
import math

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase

class SymFuncGcd( symFuncBase.SymFuncBase ):
  """
  Greatest common divisor
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name      = "gcd"
    self._desc      = "Greatest common divisor"
    self._minparams = 2    # minimum number of parameters
    self._maxparams = 2    # maximum number of parameters
    self._syntax    = "gcd(<n>, <n>)"
    self._synExplain= "gcd(<n>, <n>)"

  def functionToValue( self, elem:None|symexpress3.TypVarSym3Object ) -> None|symexpress3.TypVarSym3Object :

    if self._checkCorrectFunction( elem ) != True:
      return None

    elem = typing.cast( symexpress3.SymFunction, elem )

    elem1 = elem.elements[0]
    if not isinstance( elem1, symexpress3.SymNumber ):
      return None

    if elem1.factDenominator != 1:
      return None

    elem2 = elem.elements[1]
    if not isinstance( elem2, symexpress3.SymNumber ):
      return None

    if elem2.factDenominator != 1:
      return None

    # ignore sign answer is always positive
    valGcd = math.gcd( elem1.factCounter, elem2.factCounter )

    elemnew = symexpress3.SymNumber( 1, valGcd, 1)

    elemnew.powerSign        = elem.powerSign
    elemnew.powerCounter     = elem.powerCounter
    elemnew.powerDenominator = elem.powerDenominator

    return elemnew


  def _getValueSingle( self, dValue:symexpress3.TypVarSym3Value, dValue2:None|symexpress3.TypVarSym3Value = None ) -> symexpress3.TypVarSym3Value :
    dResult = math.gcd( int(dValue), int(dValue2) ) # type:ignore
    return dResult


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """
  def _Check( testClass :SymFuncGcd
            , symTest   :symexpress3.TypVarSym3Object
            , value     :None|symexpress3.TypVarSym3Object
            , dValue    :symexpress3.TypVarSym3Value
            , valueCalc :str
            , dValueCalc:symexpress3.TypVarSym3Value
            ) -> None :

    if dValue != None:
      dValue = symexpress3.SymRound( dValue, 10 )

    if dValueCalc != None:
      dValueCalc = symexpress3.SymRound( dValueCalc, 10 )

    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ).strip() != valueCalc or (dValueCalc != None and dValue != dValueCalc) : # pylint: disable=consider-using-in
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value} <> {valueCalc}, dValue:{dValue} <> {dValueCalc}' )

  symTest = symexpress3.SymFormulaParser( 'gcd( 2 ,10 )' )
  symTest.optimize()
  exp    = SymFuncGcd()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = exp.getValue(        symTest.elements[ 0 ] )

  _Check( exp, symTest, value, dValue, "2", 2 )


  symTest = symexpress3.SymFormulaParser( 'gcd( -35 ,100 )' )
  symTest.optimize()
  exp    = SymFuncGcd()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = exp.getValue(        symTest.elements[ 0 ] )

  _Check( exp, symTest, value, dValue, "5", 5 )



if __name__ == '__main__':
  Test( True )
