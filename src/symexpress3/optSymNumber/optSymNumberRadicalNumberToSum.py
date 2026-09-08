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


    https://en.wikipedia.org/wiki/Binomial_series


"""
import typing

from symexpress3 import symexpress3
from symexpress3 import optTypeBase
from symexpress3 import symtools

class OptSymNumberRadicalNumberToSum( optTypeBase.OptTypeBase ):
  """
  Convert radical integers into a sum
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "radicalNumberToSum"
    self._symtype      = symexpress3.SymNumber
    self._desc         = "Convert radical integers into a sum"

  def optimize( self, elem:symexpress3.TypVarSym3Object, action:None|str ) -> None|symexpress3.TypVarSym3Object:

    if self.checkType( elem, action ) != True:
      return None

    elem = typing.cast( symexpress3.SymNumber, elem )

    if elem.onlyOneRoot != 1:
      return None

    if elem.factSign == -1 : # this is an imaginary number, see optimizeOnlyOneRoot.py
      return None

    if elem.powerDenominator <= 1: # see optimizeOnlyOneRoot.py
      return None

    if elem.factCounter in (0, 1) :
      return None

    elemNum = elem.copy()
    elemNum.powerSign        = 1
    elemNum.powerCounter     = 1
    elemNum.powerDenominator = 1

    expNum = symexpress3.SymExpress( '+' )
    expNum.add( symexpress3.SymNumber( -1,1,1 )) # -1
    expNum.add( elemNum )

    elemPower = symexpress3.SymNumber( elem.powerSign, elem.powerCounter, elem.powerDenominator )
    elemVar   = symexpress3.SymVariable( symtools.VariableGenerateGet() )

    elemSum = symexpress3.SymFunction( 'sum' )
    elemSum.add( elemVar )
    elemSum.add( symexpress3.SymNumber( 1,0, 1))  # zero
    elemSum.add( symexpress3.SymVariable( 'infinity'))

    elemMult = symexpress3.SymExpress( '*' )

    elemFunc = symexpress3.SymFunction( 'binomial' )
    elemFunc.add( elemPower )
    elemFunc.add( elemVar   )

    elemMult.add( elemFunc )

    elemExp = symexpress3.SymFunction( 'exp' )
    elemExp.add( elemVar )
    elemExp.add( expNum  )

    elemMult.add( elemExp )


    elemSum.add( elemMult )

    return elemSum

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """
  symtools.VariableGenerateReset()

  symTest = symexpress3.SymNumber( 1, 2, 3, 1, 1, 3, 1 ) #  (2/3)^^(1/3)

  testClass = OptSymNumberRadicalNumberToSum()
  symNew    = testClass.optimize( symTest, "radicalNumberToSum" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "sum( n1,0,infinity, binomial( (1/3),n1 ) *  exp( n1,(-1) + (2/3) ) )":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymNumber optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )


if __name__ == '__main__':
  Test( True )
