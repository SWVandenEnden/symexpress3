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
import typing

from symexpress3          import symexpress3
from symexpress3.optimize import optimizeBase

class OptimizeRadicalFractionToWhole( optimizeBase.OptimizeBase ):
  """
  Change a radical fraction to a whole number
  \n 25 * (2/5)^^(1/2) -> 5 * (10)^^(1/2)
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "radicalFractionToWhole"
    self._symtype      = "*"
    self._desc         = "Change a radical fraction to a whole number, 25 * (2/5)^^(1/2) -> 5 * (10)^^(1/2)"


  def optimize( self, symExpr:symexpress3.TypVarSym3Object, action:None|str ) -> bool:
    result = False

    # symexpress3.SymExpressTree( symExpr )

    if self.checkExpression( symExpr, action ) != True:
      return result

    # set type for mypy
    # https://mypy.readthedocs.io/en/stable/type_narrowing.html
    symExpr = typing.cast( symexpress3.SymExpress, symExpr )

    # needed 1 number and a list of fractions
    varSymNumber:None|symexpress3.SymNumber    = None
    lstSymNumber:list[ symexpress3.SymNumber ] = []

    for elem in symExpr.elements:
      if not isinstance( elem, symexpress3.SymNumber ):
        continue

      if elem.onlyOneRoot != 1:
        continue

      if elem.powerSign != 1:
        continue

      if elem.powerCounter == 1 and elem.powerDenominator == 1:
        # need only 1 number
        if varSymNumber == None:
          varSymNumber = elem
      elif elem.powerCounter == 1 and elem.powerDenominator > 1:
        if elem.factDenominator > 1:
          lstSymNumber.append( elem )

    # check something to do
    if varSymNumber == None:
      return False

    if len( lstSymNumber ) == 0:
      return False

    result = True

    # powerCounter is always 1
    for elemNum in lstSymNumber:
      newFact    = elemNum.factDenominator ** ( elemNum.powerDenominator - 1 )
      newCounter = elemNum.factCounter * newFact

      # update number outside radical
      varSymNumber.factDenominator = varSymNumber.factDenominator * elemNum.factDenominator

      # update radical, no fraction anymore
      elemNum.factCounter      = newCounter
      elemNum.factDenominator  = 1

    return result

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """
  def _Check( testClass:OptimizeRadicalFractionToWhole
            , symOrg   :symexpress3.TypVarSym3Object
            , symTest  :symexpress3.TypVarSym3Object
            , wanted   :str
            ) -> None :

    if display == True :
      print( f"naam      : {testClass.name}" )
      print( f"orginal   : {str( symOrg  )}" )
      print( f"optimized : {str( symTest )}" )

    if str( symTest ).strip() != wanted:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}' )

  symTest:symexpress3.TypVarSym3Object = symexpress3.SymFormulaParser( '25 * (2/5)^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply")
  symTest.optimize()
  symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symTest = symTest.elements[ 0 ]
  symOrg:symexpress3.TypVarSym3Object = symTest.copy()

  testClass = OptimizeRadicalFractionToWhole()
  testClass.optimize( symTest, "radicalFractionToWhole" )

  _Check( testClass, symOrg, symTest, "(25/5) * 10^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( '25 * (2/5)^^(1/2) * (5/17)^^(1/5)' )
  symTest.optimize()
  symTest.optimize( "multiply")
  symTest.optimize()
  # symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeRadicalFractionToWhole()
  testClass.optimize( symTest, "radicalFractionToWhole" )

  _Check( testClass, symOrg, symTest, "(25/85) * 10^^(1/2) * 417605^^(1/5)" )


if __name__ == '__main__':
  Test( True )
