#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Dedekind eta function for Sym Express 3

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

    https://en.wikipedia.org/wiki/Dedekind_eta_function
"""

import mpmath

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase


class SymFuncDedekindEta( symFuncBase.SymFuncBase ):
  """
  Dedeking eta function
  """
  __slots__ = ()

  def __init__( self ):
    super().__init__()
    self._name        = "dedekindeta"
    self._desc        = "Dedeking eta function"
    self._minparams   = 1      # minimum number of parameters
    self._maxparams   = 1      # maximum number of parameters
    self._syntax      = "dedekindeta( <n> )"
    self._synExplain  = "dedekindeta( <n> )"

  def mathMl( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return [], None

    output = ""

    # https://www.compart.com/en/unicode/U+1D702
    output += '<mi>&#120578;</mi>'
    output += elem.mathMlParameters()

    return [], output


  def functionToValue( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None

    if elem.numElements() != 1:
      return None

    # for the moment no transformation
    return None

  def _getValueSingle( self, dValue, dValue2 = None ):
    return mpmath.eta( dValue  )


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check( testClass, symTest, value, dValue, valueCalc, dValueCalc ):

    if dValue != None:
      dValue = symexpress3.SymRound( dValue, 10 )

    if dValueCalc != None:
      # dValueCalc = round( float(dValueCalc), 10 )
      dValueCalc = symexpress3.SymRound( dValueCalc, 10 )

    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if valueCalc != None:
      if str( value ).strip() != valueCalc.strip() or (dValueCalc != None and dValue != dValueCalc) : # pylint: disable=consider-using-in
        print( f"Error unit test {testClass.name} function" )
        raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value} <> {valueCalc}, dValue:{dValue} <> {dValueCalc}' )

  symTest = symexpress3.SymFormulaParser( 'eta( 1 + i )' )
  symTest.optimize()

  testClass = SymFuncDedekindEta()

  # no idea why it said it is none
  # pylint: disable=assignment-from-none
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check( testClass, symTest, value, dValue, None, 0.7420487758365 + 0.19883137022j )


if __name__ == '__main__':
  Test( True )
