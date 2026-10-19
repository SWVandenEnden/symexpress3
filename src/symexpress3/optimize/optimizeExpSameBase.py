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

class OptimizeExpSameBase( optimizeBase.OptimizeBase ):
  """
  Add exp together with the same base.
  \n exp( 3^^(1/2) ) * exp( 5^^(1/2) ) = exp( 3^^(1/2) + 5^^(1/2) )
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "expSameBase"
    self._symtype      = "*"
    self._desc         = "Add exp together with the same base"


  def optimize( self, symExpr:symexpress3.TypVarSym3Object, action:None|str ) -> bool:
    result = False

    # symexpress3.SymExpressTree( symExpr )

    if self.checkExpression( symExpr, action ) != True:
      return result

    symExpr = typing.cast( symexpress3.SymExpress, symExpr )
    numExpr = symExpr.numElements()

    if numExpr <= 1:
      return result

    arrDel:set[int]  = set()
    arrSkip:set[int] = set()

    for iCnt in range( 0, numExpr ):
      if iCnt in arrSkip:
        continue
      elemFunc = symExpr.elements[ iCnt ]

      if elemFunc.powerIsOne() != True:
        continue

      if elemFunc.classType != symexpress3.CLASSTYPE_SYMFUNCTION:
        continue

      elemFunc = typing.cast( symexpress3.SymFunction, elemFunc )

      if elemFunc.name != 'exp':
        continue

      arrSkip.add( iCnt )

      numFunc = elemFunc.numElements()
      if numFunc < 1 or numFunc > 2:
        continue

      # ok, found a valid exp function
      # now get base
      elemBase:symexpress3.TypVarSym3Object
      if numFunc == 1:
        elemBase = symexpress3.SymVariable( 'e' )
      else:
        elemBase = elemFunc.elements[1]

      # only support base element with power of 1
      if elemBase.powerIsOne() == False:
        continue

      for iCnt2 in range( 0, numExpr ):
        if iCnt2 in arrSkip:
          continue

        elem2  = symExpr.elements[ iCnt2 ]
        lFound = False

        if elem2.classType == symexpress3.CLASSTYPE_SYMFUNCTION:

          elem2 = typing.cast( symexpress3.SymFunction, elem2 )

          if elem2.name == 'exp' and elem2.powerIsOne() == True:
            numFunc2 = elem2.numElements()

            elemBase2:None|symexpress3.TypVarSym3Object = None

            if numFunc2 == 1:
              elemBase2 = symexpress3.SymVariable( 'e' )
            elif numFunc2 == 2:
              elemBase2 = elem2.elements[ 1 ]

            if elemBase2 != None:
              if elemBase.isEqual( elemBase2 ):
                lFound = True
                result = True

                arrDel.add(  iCnt2 )
                arrSkip.add( iCnt2 )

                # add powers
                symPower = symexpress3.SymExpress( '+' )
                symPower.elements.append( elemFunc.elements[ 0 ] )
                symPower.elements.append( elem2.elements[    0 ] )

                elemFunc.elements[ 0 ] = symPower

        if lFound == True :
          continue

        if elemBase.classType != elem2.classType:
          continue

        if elemBase.onlyOneRoot != 1:
          continue

        if elemBase.isEqual( elem2, True, False) == True:
          result = True

          arrDel.add(  iCnt2 )
          arrSkip.add( iCnt2 )

          symPower = symexpress3.SymExpress( '+' )
          symPower.elements.append( elemFunc.elements[ 0 ] )

          symPower2 = symexpress3.SymNumber()
          symPower2.factSign        = elem2.powerSign
          symPower2.factCounter     = elem2.powerCounter
          symPower2.factDenominator = elem2.powerDenominator

          symPower.elements.append( symPower2 )

          elemFunc.elements[0] = symPower


    # del elements
    for iCnt in sorted( arrDel, reverse=True):
      del symExpr.elements[ iCnt ]


    return result

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """
  def _Check( testClass:OptimizeExpSameBase
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

  symTest:symexpress3.TypVarSym3Object = symexpress3.SymFormulaParser( 'exp( 3^^(1/2) ) * exp( 5^^(1/2) )' )
  symTest.optimize()
  symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symTest = symTest.elements[ 0 ]
  symOrg:symexpress3.TypVarSym3Object = symTest.copy()

  testClass = OptimizeExpSameBase()
  testClass.optimize( symTest, "expSameBase" )

  _Check( testClass, symOrg, symTest, "exp( 3^^(1/2) + 5^^(1/2) )" )


  symTest = symexpress3.SymFormulaParser( 'exp( 3^^(1/2) ) * e' )
  symTest.optimize()
  # symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symTest = symTest.elements[ 0 ]
  symOrg  = symTest.copy()

  testClass = OptimizeExpSameBase()
  testClass.optimize( symTest, "expSameBase" )

  _Check( testClass, symOrg, symTest, "exp( 3^^(1/2) + 1 )" )


  symTest = symexpress3.SymFormulaParser( '3 * exp( 3^^(1/2), pi ) * e * exp( g^^(1/2), pi )' )
  symTest.optimize()
  # symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symTest = symTest.elements[ 0 ]
  symOrg  = symTest.copy()

  testClass = OptimizeExpSameBase()
  testClass.optimize( symTest, "expSameBase" )

  _Check( testClass, symOrg, symTest, "3 *  exp( 3^^(1/2) + g^^(1/2),pi ) * e" )


if __name__ == '__main__':
  Test( True )
