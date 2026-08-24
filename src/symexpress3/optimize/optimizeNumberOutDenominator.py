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
import math

from symexpress3          import symexpress3
from symexpress3.optimize import optimizeBase

class OptimizeNumberOutDenominator( optimizeBase.OptimizeBase ):
  """
  Get number of out denominator
  \n 1/(4a+4b) into 1/4 * 1/(a+b)
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "numberOutDenominator"
    self._symtype      = "+"
    self._desc         = "Number out of denominator, 1/(4a+4b) = 1/4 * 1/(a+b)"


  def optimize( self, symExpr:symexpress3.TypVarSym3Object, action:None|str ) -> bool:

    result = False

    if self.checkExpression( symExpr, action ) != True:
      return result

    symExpr = typing.cast( symexpress3.SymExpress, symExpr )

    if symExpr.power != -1:
      return result

    if symExpr.numElements() < 2:
      return result

    listNumbers:list[symexpress3.SymNumber] = []
    for elem in symExpr.elements:
      if isinstance( elem, symexpress3.SymNumber ):
        if elem.power != 1:
          return False
        listNumbers.append( elem )
      elif isinstance( elem, symexpress3.SymExpress):
        if elem.symType != '*':
          return False
        if elem.power != 1:
          return False

        foundNumber = False
        for elemSub in elem.elements:
          if isinstance( elemSub, symexpress3.SymNumber ):
            if elemSub.power != 1:
              continue
            foundNumber = True
            listNumbers.append( elemSub )
            break

        if foundNumber == False:
          return False
      else:
        # oke, no number and not an expression with a number, do nothing
        return False

    # get counter & denominator counter
    iCounter     = 0
    iDenominator = 0
    iSign        = 0
    for elemNum in listNumbers:
      if iCounter == 0:
        iCounter     = elemNum.factCounter
        iDenominator = elemNum.factDenominator
        iSign        = elemNum.factSign
      else:
        iSign        = max( iSign, elemNum.factSign )
        iCounter     = math.gcd( elemNum.factCounter    , iCounter,   )
        iDenominator = math.gcd( elemNum.factDenominator, iDenominator)

    if iCounter == 1 and iDenominator == 1:
      return False

    # adjust numbers
    for elemNum in listNumbers:
      if iSign < 0:
        elemNum.factSign = 1
      elemNum.factCounter     = elemNum.factCounter     // iCounter
      elemNum.factDenominator = elemNum.factDenominator // iDenominator


    # adjust expression
    numNew = symexpress3.SymNumber( iSign, iCounter, iDenominator, -1, 1, 1, 1 )

    expressNew = symexpress3.SymExpress( '+' )
    expressNew.elements = symExpr.elements
    expressNew.powerSign        = symExpr.powerSign
    expressNew.powerCounter     = symExpr.powerCounter
    expressNew.powerDenominator = symExpr.powerDenominator

    symExpr.powerSign        = 1
    symExpr.powerCounter     = 1
    symExpr.powerDenominator = 1
    symExpr.elements         = []
    symExpr.symType          = '*'
    symExpr.elements.append( numNew )
    symExpr.elements.append( expressNew )

    result = True


    return result
#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """
  def _Check( testClass :OptimizeNumberOutDenominator
            , symOrg    :symexpress3.TypVarSym3Object
            , symTest   :symexpress3.TypVarSym3Object
            , wanted    :str
            ) -> None :

    if display == True :
      print( f"naam      : {testClass.name}" )
      print( f"orginal   : {str( symOrg  )}" )
      print( f"optimized : {str( symTest )}" )

    if str( symTest ).strip() != wanted:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}' )

  symTest:symexpress3.TypVarSym3Object = symexpress3.SymFormulaParser( '1/(4a+4b)' )
  symTest.optimize()
  symTest = typing.cast( symexpress3.SymExpress, symTest ) # special for mypy
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeNumberOutDenominator()
  testClass.optimize( symTest, "numberOutDenominator" )

  _Check( testClass, symOrg, symTest, "4^^-1 * (1 * a + 1 * b)^^-1" )


  symTest = symexpress3.SymFormulaParser( '1/(6a+12b+4)' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeNumberOutDenominator()
  testClass.optimize( symTest, "numberOutDenominator" )

  _Check( testClass, symOrg, symTest, "2^^-1 * (3 * a + 6 * b + 2)^^-1" )

if __name__ == '__main__':
  Test( True )
