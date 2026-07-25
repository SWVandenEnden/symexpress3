#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Binomial function for Sym Express 3

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


    https://en.wikipedia.org/wiki/Binomial_theorem

"""

import typing
import math

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase


class SymFuncBinomial( symFuncBase.SymFuncBase ):
  """
  Binomial function, x over y  = x! / ( y! * (x - y)!)
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name        = "binomial"
    self._desc        = "Binomial x over y  = x! / ( y! * (x - y)!)"
    self._minparams   = 2    # minimum number of parameters
    self._maxparams   = 2    # maximum number of parameters
    self._syntax      = "binomial(<n>,<k>)"
    self._synExplain  = "binomial(<n>,<k>) = n!/(n!(n - k)!)"

  def mathMl( self, elem:None|symexpress3.TypVarSym3Object ) -> tuple[list[str], None|str]:
    if self._checkCorrectFunction( elem ) != True:
      return [], None

    elem = typing.cast( symexpress3.SymFunction, elem )

    output = ""

    output += "<mrow><mo>(</mo>"

    output += "<mtable>"

    output += "<mtr>"
    output += "<mtd>"
    output += elem.elements[ 0 ].mathMl()
    output += "</mtd>"
    output += "</mtr>"

    output += "<mtr>"
    output += "<mtd>"
    output += elem.elements[ 1 ].mathMl()
    output += "</mtd>"
    output += "</mtr>"

    output += "</mtable>"
    output += "<mo>)</mo></mrow>"

    return [], output


  def functionToValue( self, elem:None|symexpress3.TypVarSym3Object ) -> None|symexpress3.TypVarSym3Object :

    if self._checkCorrectFunction( elem ) != True:
      return None

    elem = typing.cast( symexpress3.SymFunction, elem )

    elem1 = elem.elements[ 0 ]
    elem2 = elem.elements[ 1 ]

    # x over y  = x! / ( y! * (x - y)!)
    # (x)
    # (y)
    if not isinstance( elem1, symexpress3.SymNumber):
      return None

    if elem1.power != 1:
      return None

    if elem1.factSign == -1:
      return None

    if elem1.factDenominator != 1:
      return None


    if not isinstance( elem2, symexpress3.SymNumber ):
      return None

    if elem2.power != 1:
      return None

    if elem2.factSign == -1:
      return None

    if elem2.factDenominator != 1:
      return None

    dValue  = math.comb( elem1.getValue(), elem2.getValue() ) # type:ignore
    elemnew = symexpress3.SymFormulaParser( str( dValue ))

    elemnew.powerSign        = elem.powerSign
    elemnew.powerCounter     = elem.powerCounter
    elemnew.powerDenominator = elem.powerDenominator

    return elemnew

  def _getValueSingle( self, dValue:symexpress3.TypVarSym3Value, dValue2:None|symexpress3.TypVarSym3Value = None ) -> symexpress3.TypVarSym3Value :
    return math.comb( dValue, dValue2 ) # type:ignore

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """
  def _Check( testClass :SymFuncBinomial
            , symTest   :symexpress3.TypVarSym3Object
            , value     :None|symexpress3.TypVarSym3Object
            , dValue    :symexpress3.TypVarSym3Value
            , valueCalc :str
            , dValueCalc:symexpress3.TypVarSym3Value
            ) -> None :

    dValue     = symexpress3.SymRound( dValue    , 10 )
    dValueCalc = symexpress3.SymRound( dValueCalc, 10 )

    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ).strip() != valueCalc or dValue != dValueCalc:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value} <> {valueCalc}, dValue:{dValue} <> {dValueCalc}' )

  symTest = symexpress3.SymFormulaParser( 'binomial( 7, 5 )' )
  symTest.optimize()
  testClass = SymFuncBinomial()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "21", 21 )

if __name__ == '__main__':
  Test( True )
