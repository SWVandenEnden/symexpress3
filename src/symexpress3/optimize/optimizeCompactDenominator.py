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

class OptimizeCompactDenominator( optimizeBase.OptimizeBase ):
  """
  Compact denominator
  \n -a-1+a^^2/(a+1) = (-2a-1)/(a+1)
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "compactDenominator"
    self._symtype      = "+"
    self._desc         = "Compact denominator -a-1+a^^2/(a+1) = (-2a-1)/(a+1)"

  def optimize( self, symExpr:symexpress3.TypVarSym3Object, action:None|str ) -> bool:

    def _findParts( symExpr:symexpress3.SymExpress
                  , arrDemo:list[dict[str,typing.Any]]
                  ) -> None :
      """
      Find all the different 1/(...) and but them in arrDemo
      """
      dictDemo:dict[str,typing.Any] = {}

      for iPos, elem in enumerate( symExpr.elements):
        if not isinstance( elem, symexpress3.SymExpress ):
          continue

        # print( f"Check element: {iPos}, {str(elem)}")

        # elem = typing.cast( symexpress3.SymExpress, elem )
        if elem.symType != '*':
          continue

        if elem.power != 1:
          continue

        if elem.numElements() <= 1:
          continue

        dictDemo = {}

        # now seek 1/a+b in elem
        for iPosSub, elemSub in enumerate( elem.elements):
          if not isinstance( elemSub, symexpress3.SymExpress ):
            continue
          if elemSub.powerSign != -1:
            continue

          # for the moment no powers of radicals
          if elemSub.powerCounter != 1:
            continue

          if elemSub.powerDenominator != 1:
            continue


          if elemSub.symType != '+':
            continue
          if elemSub.numElements() <= 1:
            continue

          # print( f"create dictDemo: {str(elemSub)}")

          # ok found x/(a+b)
          # splits into x and 1/(a+b)
          dictDemo = {}
          dictDemo[ 'original'   ] = elemSub
          dictDemo[ 'posOrg'     ] = iPos
          dictDemo[ 'posSub'     ] = iPosSub
          dictDemo[ 'counterPart'] = symexpress3.SymExpress('*')
          dictDemo[ 'elemParts'  ] = symexpress3.SymExpress('+')
          dictDemo[ 'elemPos'    ] = [ iPos ]
          dictDemo[ 'elemParts'  ].elements.append( dictDemo[ 'counterPart'] )

          for iPosCntPort, elemSubPart in enumerate( elem.elements):
            if iPosCntPort == iPosSub:
              continue
            dictDemo[ 'counterPart'].elements.append( elemSubPart )

          break
        # nothing found, next element
        if len( dictDemo ) == 0:
          continue

        lFound = False
        # for iCntDemo, oDemo in enumerate( arrDemo ):
        for oDemo in arrDemo :
          orgDemo = oDemo[ 'original']
          if orgDemo.isEqual( dictDemo[ 'original' ] ):
            # ok found another element
            # print( f"Update arrDemo record: posSub: {dictDemo[ 'posSub'     ]}")
            lFound = True
            oDemo[ 'elemParts' ].elements.append( dictDemo[ 'counterPart']    )
            oDemo[ 'elemPos'   ].append(          dictDemo[ 'elemPos'    ][0] )

            break

        if lFound == False:
          # start of 1/(a+b) search
          # print( "Create arrDemo record")
          arrDemo.append( dictDemo )

    def _checkValid( oDemo       :dict[str,typing.Any]
                   , elemParts   :symexpress3.SymExpress
                   ) -> bool :
      """
      Check of elemParts are valid
      """

      # optimize internal structure for compare
      elemParts.optimize()

      if oDemo[ 'elemParts'].numElements() != elemParts.numElements():
        return False

      # safety check, need 2 elmements at least
      if oDemo[ 'original'].numElements() < 2 :
        return False

      if elemParts.numElements() < 1 :
        return False

      return True


    #
    # main part of optimize()
    #
    result = False

    if self.checkExpression( symExpr, action ) != True:
      return result

    # set type for mypy
    # https://mypy.readthedocs.io/en/stable/type_narrowing.html
    symExpr = typing.cast( symexpress3.SymExpress, symExpr )

    if symExpr.numElements() <= 2:
      return False

    # search for x/(a+b+...)
    # collect all x by each (a+b+...)
    arrDemo:list[dict[str,typing.Any]] = []
    _findParts( symExpr, arrDemo )

    # print( f"found elements: {len( arrDemo )}")

    # on this point dictDemo is filled
    if len( arrDemo ) == 0:
      return False

    # for each part (1/(...) try to optimize it
    for oDemo in arrDemo :
      # print( f"orginal   : {str(oDemo[ 'original' ])}")
      # print( f"posOrg    :     {oDemo[ 'posOrg'   ]}" )
      # print( f"elemParts : {str(oDemo[ 'elemParts'])}")
      # print( f"elemPos   :     {oDemo[ 'elemPos'  ]}" )

      # make copy, don't change the originals (append was used and not add)
      elemParts = oDemo[ 'elemParts'].copy()

      # check of elemParts is valid so it can be optimized
      if _checkValid( oDemo, elemParts ) != True:
        # print( "flip not valid")
        continue

      numElemExpr        = symExpr.numElements()
      usedElem:list[int] = [0] * numElemExpr

      elemOrg:symexpress3.SymExpress = oDemo[ 'original' ] # denominator

      # mark used elements
      for iPos in oDemo[ 'elemPos' ]:
        usedElem[ iPos ] = 2

      # collect match elements
      matchElements:list[int] = []

      for iPosDeno, elemDeno in enumerate( elemOrg.elements ):
        found = False

        # match denominator elements with other element in expression
        for iPos, elemSearch in enumerate( symExpr.elements ):
          if usedElem[ iPos ] != 0:
            continue
          if elemDeno.isEqual( elemSearch, False, True ):
            usedElem[ iPos ] = 1
            matchElements.append( iPosDeno )
            found = True

            # print( f"match: elemDeno  : {str(elemDeno)}")
            # print( f"match: elemSearch: {str(elemSearch)}")
            # print( f"match: iPos: {iPos}")

            break

        # every element must have a match
        if found == False:
          return False

      # safety check
      if len( matchElements ) < elemOrg.numElements():
        return False

      # collect all the elements in a new expression
      expPlus  = symexpress3.SymExpress( '+' )
      iCntElem = 0
      for iPos, iUsed in enumerate( usedElem ):
        if iUsed in ( 0, 2 ):
          continue

        expPlus.add( symExpr.elements[ iPos ] )
        iCntElem += 1

      # print( f"expPlus  : {str(expPlus)}")
      # print( f"elemParts: {str(elemParts)}")

      iCntElem += elemParts.numElements()

      elemOrgCopy = elemOrg.copy()
      elemOrgCopy.powerSign = 1

      expMult = symexpress3.SymExpress( '*' )
      expMult.add( expPlus   )
      expMult.add( elemOrgCopy )

      # print( f"expMult: {str(expMult)}")

      expPlusNew = symexpress3.SymExpress( '+' )
      expPlusNew.elements.append( elemParts )
      expPlusNew.elements.append( expMult   )

      expPlusNew.optimizeNormal()

      # print( f"iCntElem: {iCntElem}")
      # print( f"expPlusNew.numElements(): {expPlusNew.numElements()}")
      # print( f"expPlusNew: { str(expPlusNew)}")

      # check if there are less elements in the new expression
      if iCntElem <= expPlusNew.numElements():
        return False

      # print( f"Jippie found one: {str(expPlusNew)}")

      #
      # list of elemParts (counter)
      # walk original (denominator) and match them with elements in the expression symExpr
      # keep list of used elements in SymExpr
      # need at least 2 match elements
      # replace if match elements + elements in parts > optimize match elements + elements in parts
      #

      # make all used elements zero (0)
      iLastPos = 0
      for iPos, iUsed in enumerate( usedElem ):
        if iUsed == 0:
          continue

        symExpr.elements[ iPos ] = symexpress3.SymNumber( 1, 0, 1 ) # zero
        iLastPos = iPos

      # set new expression on the last element
      expNew = symexpress3.SymExpress( '*' )
      expNew.elements.append( expPlusNew )
      expNew.elements.append( elemOrg    )

      symExpr.elements[ iLastPos ] = expNew

      result = True

    return result

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """
  def _Check( testClass:OptimizeCompactDenominator
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
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, expected: {wanted}, value: {str( symOrg )}' )

  symTest:symexpress3.SymExpress = symexpress3.SymFormulaParser( '-a-1+a^^2/(a+1)' )
  symTest.optimizeNormal()
  # symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symOrg:symexpress3.TypVarSym3Object = symTest.copy()

  testClass = OptimizeCompactDenominator()
  testClass.optimize( symTest, "compactDenominator" )

  _Check( testClass, symOrg, symTest, "0 + 0 + (a * (-2) + (-1)) * (a + 1)^^-1" )




if __name__ == '__main__':
  Test( True )
