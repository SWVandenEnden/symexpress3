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

class OptimizeCompositeDenominator( optimizeBase.OptimizeBase ):
  """
  Composite denominator
  \n a/(a+b) + b/(a+b) = 1
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "compositeDenominator"
    self._symtype      = "+"
    self._desc         = "Composite denominator a/(a+b) + b/(a+b) = 1"

  def optimize( self, symExpr:symexpress3.TypVarSym3Object, action:None|str ) -> bool:
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
    # is number of elements equal
    # yes -> optimize counter
    # -> remove same element in each counter element
    # -> counter and denominator equal -> found one...
    #
    dictDemo:dict[str,typing.Any]      = {}
    arrDemo:list[dict[str,typing.Any]] = []

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

    # print( f"found elements: {len( arrDemo )}")

    # on this point dictDemo is filled
    if len( arrDemo ) == 0:
      return False


    # for iCntDemo, oDemo in enumerate( arrDemo ):
    for oDemo in arrDemo :
      # print( f"Check demo: {    iCntDemo}")
      # print( f"orginal   : {str(oDemo[ 'original' ])}")
      # print( f"posOrg    :     {oDemo[ 'posOrg'   ]}" )
      # print( f"elemParts : {str(oDemo[ 'elemParts'])}")
      # print( f"elemPos   :     {oDemo[ 'elemPos'  ]}" )

      # make copy, don't change the originals (append was used and not add)
      elemParts = oDemo[ 'elemParts'].copy()

      # optimize internal structure for compare
      elemParts.optimize()

      # safety check
      if oDemo[ 'elemParts'].numElements() != elemParts.numElements():
        continue

      if oDemo[ 'original' ].numElements() < elemParts.numElements():
        # more parts in the counter then in the denominator
        # delete the parts that do not match
        elemOrg    = oDemo[ 'original' ]
        checkParts = True
        while checkParts == True:
          checkParts = False
          for elemPos, elemPart in enumerate( elemParts.elements ):
            lFound = False
            for elem0 in elemOrg.elements:
              if elem0.isEqual( elemPart, False, True ):
                lFound = True
                break
            if lFound == False:
              del elemParts.elements[ elemPos ]
              del oDemo[ 'elemPos' ][ elemPos ]
              checkParts = True
              break


      # number of elements must be equal otherwise it will not be equal...
      if oDemo[ 'original' ].numElements() != elemParts.numElements():
        continue

      # print( "Tree original")
      # symexpress3.SymExpressTree( oDemo[ 'original'  ] )
      # print( " ")

      # print( "Tree parts")
      # symexpress3.SymExpressTree( elemParts )
      # print( " ")

      # from pudb import set_trace; set_trace()

      isEqual = oDemo[ 'original' ].isEqual( elemParts, True, False )

      equalElements = []
      if isEqual != True:
        # search for a part that exist in all elemParts -> a c + b c -> find c
        # and get that out of elemParts...
        elem0 = elemParts.elements[ 0 ]

        # print( f"elem0    : {str(elem0)}")
        # print( f"elemParts: {str(elemParts)}")

        if isinstance( elem0, symexpress3.SymExpress ) and elem0.symType == '*':

          # ok search for each elements if it contains in the others

          # collect all the elements in the first part
          for elem0Part in elem0.elements:
            equalElements.append( elem0Part)

          # print( f"equalElements: {str(equalElements)}")

          # search in the other parts for equal elements
          for elemNr, elemNext in enumerate( elemParts.elements ):
            # skip yourself = first element
            if elemNr == 0:
              continue

            if not isinstance( elemNext, symexpress3.SymExpress):
              # print( f"Not SymExpress, stop: {str(elemNext)}")
              equalElements = []
              break


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

            for elemE in equalElements:
              for elemNr, elemP in enumerate( elemPart.elements ):
                if elemP.isEqual( elemE ):
                  elemPart.elements[ elemNr ] = symexpress3.SymNumber( 1, 1,1, 1, 1,1,1) # one


          elemParts.optimize()
          isEqual = oDemo[ 'original' ].isEqual( elemParts, True, False )

        if isEqual == False:
          # check if there is a factor different between elemParts and original

          # print( f"elemParts: {str(elemParts )}")
          # print( f"orignal: {str(oDemo[ 'original' ]) }")

          # check if there is a number in it
          numberInPart = None
          for elemPart in elemParts.elements :
            if isinstance( elemPart, symexpress3.SymNumber ):
              if elemPart.power == 1:
                numberInPart = elemPart
                break

          # ok number found, now search in orginal to number
          numberInOrg = None
          if numberInPart != None:
            for elemOrg in oDemo[ 'original' ].elements:
              if isinstance( elemOrg, symexpress3.SymNumber ):
                if elemOrg.power == 1:
                  numberInOrg = elemOrg
                  break

          # print( f"numberInPart: {str(numberInPart)}")
          # print( f"numberInOrg : {str(numberInOrg)}")

          if numberInOrg != None:
            # oke 2 numbers
            # factor for part = org / part -> org * 1 / part
            symFactPart = numberInOrg.copy()
            symFactPart.factCounter     = symFactPart.factCounter     * numberInPart.factDenominator # type:ignore
            symFactPart.factDenominator = symFactPart.factDenominator * numberInPart.factCounter     # type:ignore
            symFactPart.factSign        = symFactPart.factSign        * numberInPart.factSign        # type:ignore

            elemPartNew = symexpress3.SymExpress( '*' )
            elemPartNew.add( elemParts   )
            elemPartNew.add( symFactPart )


            # print( f"elemPartNew: {str(elemPartNew)}" )

            elemParts = elemPartNew

            # add factor to equalElements so it will be left over
            symFactPart.powerSign = -1 # inverse for the equalElements (left over) part
            equalElements.append( symFactPart )

            elemParts.optimizeNormal( extra=['nodebug'] )

            # print( f"elemParts optimized: {str(elemParts)}" )

            isEqual = oDemo[ 'original' ].isEqual( elemParts, True, False )



      if isEqual == True :
        # ok make orginal 1 (or equalElements)
        # set all others on 0 (zero)
        # print( "change expression")

        iPosOrg = oDemo[ 'posOrg' ]
        if len( equalElements ) == 0:
          symExpr.elements[ iPosOrg ] = symexpress3.SymNumber( 1, 1, 1, 1, 1, 1 ) # one
        else:
          symExpr.elements[ iPosOrg ] = symexpress3.SymExpress( '*' )
          for elem in equalElements:
            symExpr.elements[ iPosOrg ].add( elem )

        for iPosPart in oDemo[ 'elemPos' ]:
          if iPosPart == iPosOrg:
            continue
          symExpr.elements[ iPosPart ] = symexpress3.SymNumber( 1, 0, 1, 1, 1, 1 ) # zero

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
  def _Check( testClass:OptimizeCompositeDenominator
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

  symTest:symexpress3.TypVarSym3Object = symexpress3.SymFormulaParser( 'a/(a+b) + b/(a+b)' )
  symTest.optimize()
  symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symOrg:symexpress3.TypVarSym3Object = symTest.copy()

  testClass = OptimizeCompositeDenominator()
  testClass.optimize( symTest, "compositeDenominator" )

  _Check( testClass, symOrg, symTest, "1 + 0" )


  symTest = symexpress3.SymFormulaParser( 'c + a/(a+b) + d/a + b/(a+b)' )
  symTest.optimize()
  # symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symOrg = symTest.copy()

  testClass = OptimizeCompositeDenominator()
  testClass.optimize( symTest, "compositeDenominator" )

  _Check( testClass, symOrg, symTest, "c + 1 + d * a^^-1 + 0" )


  symTest = symexpress3.SymFormulaParser( 'c * a/(a+b) + c * b/(a+b)' )
  symTest.optimize()
  # symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symOrg = symTest.copy()

  testClass = OptimizeCompositeDenominator()
  testClass.optimize( symTest, "compositeDenominator" )

  _Check( testClass, symOrg, symTest, "c + 0" )


  symTest = symexpress3.SymFormulaParser( 'd * c * a/(a+b) + d * c * b/(a+b)' )
  symTest.optimize()
  # symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symOrg = symTest.copy()

  testClass = OptimizeCompositeDenominator()
  testClass.optimize( symTest, "compositeDenominator" )

  _Check( testClass, symOrg, symTest, "d * c + 0" )


  symTest = symexpress3.SymFormulaParser( '2 cos(x) sin(x) a / (a + b + 4) +  2 cos(x) sin(x) b /(a+b + 4) + 2 sin(x) 4 cos(x) / (a+b+4)' )
  symTest.optimize()
  # symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symOrg = symTest.copy()

  testClass = OptimizeCompositeDenominator()
  testClass.optimize( symTest, "compositeDenominator" )

  _Check( testClass, symOrg, symTest, "2 *  cos( x ) *  sin( x ) + 0 + 0" )



  symTest = symexpress3.SymFormulaParser( '-a / (a + b + 4 ) +  -b /(a+b+4) + -4/(a+b+4)' )
  symTest.optimize()
  # symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symOrg = symTest.copy()

  testClass = OptimizeCompositeDenominator()
  testClass.optimize( symTest, "compositeDenominator" )

  _Check( testClass, symOrg, symTest, "(-4/4)^^-1 + 0 + 0" )


  symTest = symexpress3.SymFormulaParser( 'a/(a+b+c) + b/(a+b+c) + c/(a+b+c) + d/(a+b+c)' )
  symTest.optimize()
  # symTest = typing.cast( symexpress3.SymExpress, symTest) # special for mypy
  symOrg = symTest.copy()

  testClass = OptimizeCompositeDenominator()
  testClass.optimize( symTest, "compositeDenominator" )

  _Check( testClass, symOrg, symTest, "1 + 0 + 0 + d * (a + b + c)^^-1" )


if __name__ == '__main__':
  Test( True )
