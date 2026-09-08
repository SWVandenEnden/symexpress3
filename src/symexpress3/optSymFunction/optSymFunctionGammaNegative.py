#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Negative integer gamma for Sym Express 3

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

    https://en.wikipedia.org/wiki/Gamma_function

"""

import typing

from symexpress3 import symexpress3
from symexpress3 import optFunctionBase


class OptSymFunctionGammaNegative( optFunctionBase.OptFunctionBase ):
  """
  Convert negative integer gamma into infinity
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "gammaNegative"
    self._desc         = "Convert negative integer gamma into infinity"
    self._funcName     = "gamma"                  # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 1                        # maximum number of parameters


  def optimize( self, elem:symexpress3.TypVarSym3Object, action:None|str ) -> None|symexpress3.TypVarSym3Object:

    if self.checkType( elem, action ) != True:
      return None

    elem  = typing.cast( symexpress3.SymFunction, elem )
    elem1 = elem.elements[0]

    if not isinstance( elem1, symexpress3.SymNumber ):
      return None

    if elem1.factDenominator != 1:
      return None

    if elem1.power != 1:
      return None

    if not( elem1.factCounter == 0 or elem1.factSign == -1) :
      return None

    # oke on this point we have zero or a negative integer number
    elemNew = symexpress3.SymArray()
    elemNew.add( symexpress3.SymVariable( 'infinity') )

    elemNeg = symexpress3.SymExpress( '*' )
    elemNeg.add( symexpress3.SymNumber( -1,1,1)) # -1
    elemNeg.add( symexpress3.SymVariable( 'infinity'))

    elemNew.add( elemNeg )

    elemNew.powerSign        = elem.powerSign
    elemNew.powerCounter     = elem.powerCounter
    elemNew.powerDenominator = elem.powerDenominator

    return elemNew


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """
  def _Check( testClass :OptSymFunctionGammaNegative
            , symTest   :symexpress3.TypVarSym3Object
            , symNew    :symexpress3.TypVarSym3Object
            , valueCalc :str
            ) -> None :


    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"symNew  : {str( symNew  )}" )

    if str( symNew ).strip() != valueCalc:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, symNew: {str(symNew)} <> {valueCalc}' )

  symTest:symexpress3.TypVarSym3Object = symexpress3.SymFormulaParser( 'gamma( -17 )' )
  symTest.optimize()
  symTest = symTest.elements[0] # type:ignore
  testClass = OptSymFunctionGammaNegative()
  symNew    = testClass.optimize( symTest, "gammaNegative" )


  _Check(  testClass, symTest, symNew, "[ infinity | (-1) * infinity ]" ) # type:ignore


if __name__ == '__main__':
  Test( True )
