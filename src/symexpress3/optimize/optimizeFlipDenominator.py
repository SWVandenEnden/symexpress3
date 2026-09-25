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

class OptimizeFlipDenominator( optimizeBase.OptimizeBase ):
  """
  Flip denominator
  \n a/(a+b+c) + b/(a+b+c)  = 1 - c/(a+b+c)
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "flipDenominator"
    self._symtype      = "+"
    self._desc         = "Flip denominator a/(a+b+c) + b/(a+b+c)  = 1 - c/(a+b+c)"

  def optimize( self, symExpr:symexpress3.TypVarSym3Object, action:None|str ) -> bool:

    def _findParts( symExpr:symexpress3.SymExpress
                 , arrDemo:list[dict[str,typing.Any]]
                 ) -> None :
      """
      find all the different 1/(...) and but them in arrDemo
      """
      dictDemo:dict[str,typing.Any] = {}

      for iPos, elem in enumerate( symExpr.elements):
        # if not isinstance( elem, symexpress3.SymExpress ):
        if elem.classType != symexpress3.CLASSTYPE_SYMEXPRESS :
          continue

        # print( f"Check element: {iPos}, {str(elem)}")
        elem = typing.cast( symexpress3.SymExpress, elem )

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
          # if not isinstance( elemSub, symexpress3.SymExpress ):
          if elemSub.classType != symexpress3.CLASSTYPE_SYMEXPRESS :
            continue
          if elemSub.powerSign != -1:
            continue

          # for the moment no powers of radicals
          if elemSub.powerCounter != 1:
            continue

          if elemSub.powerDenominator != 1:
            continue

          elemSub = typing.cast( symexpress3.SymExpress, elemSub )

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


    def _getMatches( oDemo     :dict[str,typing.Any]
                   , elemParts :symexpress3.SymExpress
                   , arrMatch  :list[dict[str,int]]
                   , arrOrgElem:list[int]
                   ) -> bool :
      """
      Find all the matches and store that in arrMatch, arrOrgElem contains the elements used
      """
      # for elemPos, elemPart in enumerate( elemParts.elements ):
      for elemPart in elemParts.elements :

        # remember number of elements in elemPart
        # if elempart has power != 1 then it is a one (1) element
        if elemPart.power != 1:
          numElemPart = 1
        # elif isinstance( elemPart, symexpress3.SymExpress):
        elif elemPart.classType == symexpress3.CLASSTYPE_SYMEXPRESS :
          elemPart    = typing.cast( symexpress3.SymExpress, elemPart )
          numElemPart = elemPart.numElements()
        else:
          numElemPart = 1

        currentMatch = {}
        currentMatch[ 'numElemPart'  ] = numElemPart
        currentMatch[ 'numElemOrg'   ] = 0
        currentMatch[ 'numElemMatch' ] = 0
        currentMatch[ 'number'       ] = 0

        # print( f"Start current match: {currentMatch}")
        elemOrg = oDemo[ 'original' ]
        elemOrg = typing.cast( symexpress3.SymExpress, elemOrg )

        for elemOrgPos, elem0 in enumerate( elemOrg.elements ):

          # already used
          if arrOrgElem[ elemOrgPos ] != 0:
            continue

          if elem0.power != 1:
            numElemOrg = 1
          # elif isinstance( elem0, symexpress3.SymExpress ):
          elif elem0.classType == symexpress3.CLASSTYPE_SYMEXPRESS :
            elem0      = typing.cast( symexpress3.SymExpress, elem0 )
            numElemOrg = elem0.numElements()
          else:
            numElemOrg = 1

          numElemMatch = 0

          if elem0.isEqual( elemPart, True, True ):
            # all match
            numElemMatch = numElemOrg
          else:
            if numElemOrg == 1 and numElemPart == 1:
              # numbers are special so mark it (only without power)
              # if isinstance( elem0, symexpress3.SymNumber) and isinstance( elemPart, symexpress3.SymNumber ):
              if elem0.classType == symexpress3.CLASSTYPE_SYMNUMBER and elemPart.classType == symexpress3.CLASSTYPE_SYMNUMBER :
                if elem0.power == 1 and elemPart.power == 1:
                  numElemMatch = 1
                  currentMatch[ 'number'    ] = 1

            elif numElemOrg > 1 and numElemPart == 1:
              # walk org
              elem0 = typing.cast( symexpress3.SymExpress, elem0 )

              for elemSub in elem0.elements:
                if elemSub.isEqual( elemPart, True, True ):
                  numElemMatch = 1
                  break

            elif numElemOrg == 1 and numElemPart > 1:
              # walk part
              elemPart = typing.cast( symexpress3.SymExpress, elemPart )

              for elemSub in elemPart.elements:
                if elemSub.isEqual( elem0 ):
                  numElemMatch = 1
                  break
            else:
              # walk part and org
              elemPart = typing.cast( symexpress3.SymExpress, elemPart )
              elem0    = typing.cast( symexpress3.SymExpress, elem0    )

              for elemSubPart in elemPart.elements :
                for elemSubOrg in elem0.elements:
                  if elemSubPart.isEqual( elemSubOrg ):
                    numElemMatch += 1

          # on this pos
          # numElemOrg   = number of elements in original (=denominator)
          # numElemParts = number of elements in parts (=counter)
          # numElemMatch = match number of elements

          if numElemOrg == numElemMatch:
            # found 100% match
            currentMatch[ 'numElemOrg'   ] = numElemOrg
            currentMatch[ 'numElemMatch' ] = numElemMatch
            currentMatch[ 'elemOrgPos'   ] = elemOrgPos
            break

          if numElemMatch > 0:
            # search if this is the highest match
            if currentMatch[ 'numElemMatch' ] == 0:
              currentMatch[ 'numElemOrg'   ] = numElemOrg
              currentMatch[ 'numElemMatch' ] = numElemMatch
              currentMatch[ 'elemOrgPos'   ] = elemOrgPos
            else:
              if currentMatch[ 'numElemMatch' ] / currentMatch[ 'numElemOrg'  ] > numElemMatch / numElemOrg:
                # found better match
                currentMatch[ 'numElemOrg'   ] = numElemOrg
                currentMatch[ 'numElemMatch' ] = numElemMatch
                currentMatch[ 'elemOrgPos'   ] = elemOrgPos



        # on this point, all elemOrg.elements check on current elemPart
        if currentMatch[ 'numElemMatch' ] == 0:
          # element does not match so nothing to do
          # print( f"No match {currentMatch}")
          return False

        # print( f"match {currentMatch}")

        # remember all matches
        arrMatch.append( currentMatch.copy() )

        arrOrgElem[ currentMatch[ 'elemOrgPos' ] ] = 1 # match org element as matched

      return True # oke, match found


    def _findEquals( elemParts    :symexpress3.SymExpress
                   , equalElements:list[symexpress3.TypVarSym3Object]
                   , arrMatch     :list[dict[str,int]]
                   ) -> None :
      """
      Find all the equal elements in the parts.
      Store them in equalElements[] and remove them from elemParts
      """

      # if there is 1 element with 100% match do nothing.
      for currentMatch in arrMatch:
        if currentMatch[ 'numElemPart' ] == currentMatch[ 'numElemMatch' ]:
          return

      # search for a part that exist in all elemParts -> a c + b c -> find c
      # and get that out of elemParts...
      elem0 = elemParts.elements[ 0 ]

      # print( f"elem0    : {str(elem0)}")
      # print( f"elemParts: {str(elemParts)}")

      # if isinstance( elem0, symexpress3.SymExpress ) and elem0.symType == '*':
      if elem0.classType == symexpress3.CLASSTYPE_SYMEXPRESS and elem0.symType == '*': # type:ignore

        # ok search for each elements if it contains in the others
        elem0 = typing.cast( symexpress3.SymExpress, elem0 )

        # collect all the elements in the first part
        for elem0Part in elem0.elements:
          equalElements.append( elem0Part)

        # print( f"equalElements: {str(equalElements)}")

        # search in the other parts for equal elements
        for elemNr, elemNext in enumerate( elemParts.elements ):
          # skip yourself = first element
          if elemNr == 0:
            continue

          # if not isinstance( elemNext, symexpress3.SymExpress):
          if elemNext.classType != symexpress3.CLASSTYPE_SYMEXPRESS :

            # print( f"Not SymExpress, stop: {str(elemNext)}")
            equalElements = []
            break

          elemNext = typing.cast( symexpress3.SymExpress, elemNext )

          # collect equal elements
          elemNew = []
          for elemSub in elemNext.elements :
            elemNew.append( elemSub )

          if len( elemNew ) == 0:
            equalElements = []
            break

          # check of there are equal elements
          checkAgain = True
          while checkAgain == True:

            checkAgain = False
            for elemNr, elemE in enumerate( equalElements ):

              lFoundOne = False
              for elmSub in elemNew :
                # print( f"Check equal elmSub: {str(elemSub)} - elemE: {str(elemE)}")
                if elemE.isEqual( elmSub, False, True ): # don't check factor but do check power
                  lFoundOne = True
                  break

              if lFoundOne == False:
                del equalElements[ elemNr ]
                checkAgain = True
                break

          # if len( equalElements ) == 0:
          #   equalElements = []
          #   break

      # print( f"Found equalElements: {len(equalElements)}")
      if len( equalElements ) > 0:
        # print( f"Found equalElements: {len(equalElements)}")
        # isEqual = True

        # delete same part elements from elemParts

        # print( f"elemParts: {str(elemParts)}")
        for elemPart in elemParts.elements :

          # print( f"elemPart {str(elemPart)}" )
          elemPart = typing.cast( symexpress3.SymExpress, elemPart )

          for elemE in equalElements:
            for elemNr, elemP in enumerate( elemPart.elements ):
              if elemP.isEqual( elemE ):
                elemPart.elements[ elemNr ] = symexpress3.SymNumber( 1, 1,1, 1, 1,1,1) # one


        elemParts.optimize()


    def _findFactor( oDemo    :dict[str,typing.Any]
                   , elemParts:symexpress3.SymExpress
                   , arrMatch :list[dict[str,int]]
                   ) -> None|symexpress3.SymNumber:

      # search for valid number in parts
      foundNumber = None
      posParts    = 0
      for pos, currentMatch in enumerate( arrMatch ):
        if currentMatch[ 'number' ] == 1:
          posParts    = pos
          foundNumber = currentMatch
          break

      if foundNumber == None:
        return None

      # print( f"foundNumber: {foundNumber}")
      elemOrg = oDemo[ 'original' ]
      elemOrg = typing.cast( symexpress3.SymExpress, elemOrg )

      # print( f"elemOrg: {str(elemOrg)}")

      numberInOrg  = elemOrg.elements[   foundNumber[ 'elemOrgPos'  ] ]
      numberInPart = elemParts.elements[ posParts                     ]

      numberInOrg  = typing.cast( symexpress3.SymNumber, numberInOrg  )
      numberInPart = typing.cast( symexpress3.SymNumber, numberInPart )

      # print( f"numberInOrg: {str(numberInOrg)}")
      # print( f"numberInPart: {str(numberInPart)}")

      symFactPart = numberInOrg.copy()

      symFactPart.factCounter     = symFactPart.factCounter     * numberInPart.factDenominator
      symFactPart.factDenominator = symFactPart.factDenominator * numberInPart.factCounter
      symFactPart.factSign        = symFactPart.factSign        * numberInPart.factSign
      if symFactPart.factor == 1:
        return None

      # remove factor from parts
      elemPartNew = symexpress3.SymExpress( '*' )
      elemPartNew.add( elemParts   )
      elemPartNew.add( symFactPart )

      # print( f"elemPartNew: {str(elemPartNew)}" )

      elemPartNew.optimizeNormal( extra=['nodebug'] )

      elemParts.elements = elemPartNew.elements
      elemParts.optimizeNormal( extra=['nodebug'] )

      return symFactPart



    def _createNewParts( oDemo       :dict[str,typing.Any]
                       , elemParts   :symexpress3.SymExpress
                       , elemNewParts:list[ symexpress3.TypVarSym3Object]
                       ) -> None :
      """
      Create the missing parts add them to elemPart and make a list in elemNewParts
      """

      elemOrg = oDemo[ 'original' ]
      elemOrg = typing.cast( symexpress3.SymExpress, elemOrg )

      # print( f"elemOrg: {str(elemOrg)}")

      for iPos, iVal in enumerate( arrOrgElem ):
        # if arrOrgElem[ iPos ] != 0 :
        if iVal != 0 :
          continue

        # print( "new parts create")

        elemNewPart = elemOrg.elements[ iPos ].copy()
        elemNewParts.append( elemNewPart )
        elemParts.add( elemNewPart )

      # print( "Before optimize")

      elemParts.optimize()


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

      # safety check, need 3 elmements at least
      if oDemo[ 'original'].numElements() <= 2 :
        return False

      if elemParts.numElements() < 1 :
        return False

      # print( "start check invert denominator")

      iLenOrg      = oDemo[ 'original' ].numElements()
      iLenOrgDiv2  = iLenOrg // 2
      iLenOrgCheck = iLenOrgDiv2 + 1

      # print( f"orginal: {str(oDemo[ 'original' ])}")
      # print( f"iLenOrg     : {iLenOrg}")
      # print( f"iLenOrgDiv2 : {iLenOrgDiv2}")
      # print( f"iLenOrgCheck: {iLenOrgCheck}")
      # print( f"numParts    : {elemParts.numElements()}")

      # there must less elements in the parts then de denominator. The different must be greater then the halve
      if iLenOrgCheck > elemParts.numElements():
        # print( f"Afgekeurd iLenOrgCheck: {iLenOrgCheck}, elemParts.numElements(): {elemParts.numElements()}")
        return False

      return True


    def _updateExpression( symExpr      :symexpress3.SymExpress
                         , oDemo        :dict[str,typing.Any]
                         # , elemParts    :symexpress3.SymExpress
                         , equalElements:list[symexpress3.TypVarSym3Object]
                         , symFactPart  : None|symexpress3.SymNumber
                         ) -> None :
      """
      Update the expression
      """
      # print( "Ok the match")

      # oke, found match
      iPosOrg = oDemo[ 'posOrg' ]
      iPosOrg = typing.cast( int, iPosOrg )

      if len( equalElements ) == 0:
        symExpr.elements[ iPosOrg ] = symexpress3.SymNumber( 1, 1, 1, 1, 1, 1 ) # one
      else:
        symExpr.elements[ iPosOrg ] = symexpress3.SymExpress( '*' )
        for elem in equalElements:
          symExpr.elements[ iPosOrg ].add( elem ) # type:ignore

      for iPosPart in oDemo[ 'elemPos' ]:
        if iPosPart == iPosOrg:
          continue
        symExpr.elements[ iPosPart ] = symexpress3.SymNumber( 1, 0, 1, 1, 1, 1 ) # zero

      # add the missing parts
      if symFactPart != None:
        symFactPart.powerSign = -1

      partMissing = symexpress3.SymExpress( '+' )
      for elemNew in elemNewParts:
        partDeno = symexpress3.SymExpress( '*' )
        partDeno.add( elemNew )
        partDeno.add( elemOrg )

        if symFactPart != None:
          partDeno.add( symFactPart )

        partMissing.add( partDeno )

      partMul = symexpress3.SymExpress( '*' )
      for elemNew in equalElements:
        partMul.add( elemNew )

      partMul.add( partMissing )

      symExpr.add( partMul )


    #
    # main part of optimize()
    #
    result = False

    # symexpress3.SymExpressTree( symExpr )

    if self.checkExpression( symExpr, action ) != True:
      return result

    # set type for mypy
    # https://mypy.readthedocs.io/en/stable/type_narrowing.html
    symExpr = typing.cast( symexpress3.SymExpress, symExpr )

    if symExpr.numElements() <= 1:
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


      # match the part elements
      # currentMatch:dict[str,int]   = {}
      elemOrg                      = oDemo[ 'original' ]
      arrMatch:list[dict[str,int]] = []
      arrOrgElem:list[int]         = [0] * elemOrg.numElements()

      if _getMatches( oDemo, elemParts, arrMatch, arrOrgElem ) != True :
        # print( "flip not matches")
        continue

      # oke, everything matched
      # now get the same elements out of the parts

      # print( "search for equal elements")
      equalElements:list[symexpress3.TypVarSym3Object] = []

      _findEquals( elemParts, equalElements, arrMatch )

      # find factor
      # print( f"ElemParts before: {str(elemParts)}")
      symFactPart = _findFactor( oDemo, elemParts, arrMatch )
      # print( f"ElemParts after: {str(elemParts)}")
      # print( f"symFactPart: {str(symFactPart)}")

      # print( "Check parts" )

      # create the new parts
      elemNewParts:list[ symexpress3.TypVarSym3Object] = []

      _createNewParts( oDemo, elemParts, elemNewParts )

      # print( f"New elemParts: {str(elemParts)}")
      # print( f"elemOrg     : {str(elemOrg)}")

      if elemOrg.isEqual( elemParts, True, False ):
        # print( "is equal")
        # _updateExpression( symExpr, oDemo, elemParts, equalElements )
        _updateExpression( symExpr, oDemo, equalElements, symFactPart )
        result = True

        # print( "Jippie found one")
        # print( f"new symexpr: {str(symExpr)}")

    return result

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """
  def _Check( testClass:OptimizeFlipDenominator
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

  symTest:symexpress3.TypVarSym3Object = symexpress3.SymFormulaParser( 'a/(a+b+c) + b/(a+b+c)' )
  symTest.optimize()
  symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symOrg:symexpress3.TypVarSym3Object = symTest.copy()

  testClass = OptimizeFlipDenominator()
  testClass.optimize( symTest, "flipDenominator" )

  _Check( testClass, symOrg, symTest, "1 + 0 + c * (a + b + c)^^-1" )


  symTest = symexpress3.SymFormulaParser( 'a/(a+b+4) + 4/(a+b+4)' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeFlipDenominator()
  testClass.optimize( symTest, "flipDenominator" )

  _Check( testClass, symOrg, symTest, "1 + 0 + b * (a + b + 4)^^-1" )


  symTest = symexpress3.SymFormulaParser( '2 a/(a+b+4) + 8/(a+b+4)' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeFlipDenominator()
  testClass.optimize( symTest, "flipDenominator" )

  _Check( testClass, symOrg, symTest, "1 + 0 + b * (a + b + 4)^^-1 * (4/8)^^-1" )


if __name__ == '__main__':
  Test( True )
