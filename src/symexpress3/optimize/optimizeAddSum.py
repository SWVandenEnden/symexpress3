#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Sym Express 3

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

class OptimizeAddSum( optimizeBase.OptimizeBase ):
  """
  Add sum's together
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "addSum"
    self._symtype      = "+"
    self._desc         = "Add sum's together"

  def optimize( self, symExpr:symexpress3.TypVarSym3Object, action:None|str ) -> bool:


    def _getSum( elem:symexpress3.TypVarSym3Object ) -> typing.Tuple[None|symexpress3.TypVarSym3Object,None|list[symexpress3.TypVarSym3Object] ]:
      """
      Check if elem is a sum or contains a sum.
      Give back the sum (1e) and a list of multipliers (2e)
      """
      if isinstance( elem, symexpress3.SymFunction ):
        if elem.name != "sum":
          return None, None

        if elem.numElements() != 4:
          return None, None

        return elem, None

      if isinstance( elem, symexpress3.SymExpress ):

        if not elem.symType == '*':
          return None, None

        if elem.numElements() <= 1:
          return None, None

        lstFactors:list[symexpress3.TypVarSym3Object] = []
        retSum:None|symexpress3.TypVarSym3Object      = None

        for elem1 in elem.elements:
          if isinstance( elem1, symexpress3.SymFunction ):
            if retSum == None and elem1.name == 'sum' and elem1.numElements() == 4:
              # we only take the first
              retSum = elem1
            else:
              lstFactors.append( elem1 )
          else:
            lstFactors.append( elem1 )

        if retSum != None :
          return retSum, lstFactors


      return None,None

    #
    # start function
    #
    result = False

    if self.checkExpression( symExpr, action ) != True:
      return result

    symExpr = typing.cast( symexpress3.SymExpress, symExpr )

    arrDel:list[int] = []
    lFound           = False

    for iCnt in range( 0, len( symExpr.elements ) - 1) :
      if iCnt in arrDel:
        continue

      elem1, factor1 = _getSum( symExpr.elements[ iCnt ] )
      if elem1 == None:
        continue

      for iCnt2 in range( iCnt + 1, len( symExpr.elements )) :
        if iCnt2 in arrDel:
          continue

        if lFound == True:
          elem1, factor1 = _getSum( symExpr.elements[ iCnt ] )
          lFound = False
          if elem1 == None:
            break

        elem2, factor2 = _getSum( symExpr.elements[ iCnt2 ] )
        if elem2 == None:
          continue

        elem1 = typing.cast( symexpress3.SymFunction, elem1 )
        elem2 = typing.cast( symexpress3.SymFunction, elem2 )

        # can add 2 sum if range is equal
        if not elem1.elements[1].isEqual( elem2.elements[1] ):
          continue

        if not elem1.elements[2].isEqual( elem2.elements[2] ):
          continue

        # check on correct variable
        if not isinstance( elem1.elements[0], symexpress3.SymVariable):
          continue

        if elem1.elements[0].power != 1:
          continue

        if not isinstance( elem2.elements[0], symexpress3.SymVariable):
          continue

        if elem2.elements[0].power != 1:
          continue

        # add sums
        dDictReplace = {}
        dDictReplace[ elem2.elements[0].name ] = elem1.elements[0].name
        elem2.replaceVariable( dDictReplace )

        elemNew = symexpress3.SymExpress( '+' )

        if factor1 != None :
          elemFact = symexpress3.SymExpress( '*' )
          elemFact.elements = factor1
          elemFact.elements.append( elem1.elements[3] )

          elemNew.elements.append( elemFact )
        else:
          elemNew.elements.append( elem1.elements[3] )

        if factor2 != None :
          elemFact = symexpress3.SymExpress( '*' )
          elemFact.elements = factor2
          elemFact.elements.append( elem2.elements[3] )

          elemNew.elements.append( elemFact )

        else:
          elemNew.elements.append( elem2.elements[3] )

        elem1.elements[3] = elemNew

        if factor1 != None :
          symExpr.elements[ iCnt ] = elem1


        lFound = True
        arrDel.append( iCnt2 )


    # del elements
    for iCnt in sorted( arrDel, reverse=True):
      del symExpr.elements[ iCnt ]

    return result


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Test unit
  """

  def _Check( testClass:OptimizeAddSum
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

  symTest:symexpress3.TypVarSym3Object = symexpress3.SymFormulaParser( 'sum(a,1,5,x) + sum(b,1,5,y)' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeAddSum()
  testClass.optimize( symTest, "addSum" )

  _Check( testClass, symOrg, symTest, "sum( a,1,5,x + y )" )


  symTest = symexpress3.SymFormulaParser( 'sum(a,1,5,x) - sum(b,1,5,y)' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeAddSum()
  testClass.optimize( symTest, "addSum" )

  _Check( testClass, symOrg, symTest, "sum( a,1,5,x + (-1) * y )" )



  symTest = symexpress3.SymFormulaParser( 'x * y * sum(a,1,5,x + 4 ) - sum(b,1,5,y)' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeAddSum()
  testClass.optimize( symTest, "addSum" )

  _Check( testClass, symOrg, symTest, "sum( a,1,5,x * y * (x + 4) + (-1) * y )" )


if __name__ == '__main__':
  Test( True )
