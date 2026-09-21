#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Write out roots in there lowest form for Sym Express 3

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



"""

import typing

from symexpress3          import symexpress3
from symexpress3.optimize import optimizeBase
from symexpress3          import primefactor

class OptimizeOnlyOneRoot( optimizeBase.OptimizeBase ):
  """
  Write out roots in there lowest form
  \n 27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "onlyOneRoot"
    self._symtype      = "all"
    self._desc         = "Write out roots in there lowest form"


  # 27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)
  def _numberOptimize( self, symExpr:symexpress3.SymExpress ) -> bool :
    result = False

    # 27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)

    # print( "_writeOutOnlyOneRoot start" )

    # simplify the factCounter
    # 27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)
    # for iCnt in range( 0, len( symExpr.elements )):
    for iCnt, elem in enumerate( symExpr.elements ) :
      # elem = symExpr.elements[ iCnt ]

      if elem.powerDenominator == 1 :
        continue

      if not isinstance( elem, symexpress3.SymNumber ):
        continue
      # print( "elem.onlyOneRoot: {} {}".format( elem.onlyOneRoot, elem ) )
      if elem.onlyOneRoot != 1:
        continue
      if elem.factSign != 1 :
        continue
      if elem.factCounter == 1:
        # if ( elem.powerSign == 1 and elem.powerCounter == 1 and elem.factDenominator == 1 ):
        if elem.powerIsOne() == True:
          elem.powerDenominator = 1
        continue

      # print( "OnlyOneRout: " + str( elem ))
      # symFact = SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
      # symDeno = SymExpress( '*', elem.powerSign, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)
      symFact = symexpress3.SymExpress( '*', 1, 1, 1, elem.onlyOneRoot )
      symDeno = symexpress3.SymExpress( '*', 1, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)

      lFoundOne = False
      dPrimeSet = primefactor.FactorizationDict( elem.factCounter )
      for iPrime, iCount in dPrimeSet.items():
        # print( "iPrime: {}, iCount: {}, elem.powerDenominator: {}".format( iPrime, iCount,elem.powerDenominator ))
        if iCount >= elem.powerDenominator :
          iFact = iCount // elem.powerDenominator
          iRad  = iCount % elem.powerDenominator
          lFoundOne = True

          elem1 = symexpress3.SymNumber( 1, int( iPrime ), 1, 1, iFact, 1, 1 )
          # symFact.add ( elem1 )
          symFact.elements.append( elem1 )

          if iRad > 0 :
            elem1 = symexpress3.SymNumber( 1, int( iPrime ), 1, 1, iRad, 1, 1 )
            # symDeno.add ( elem1 )
            symDeno.elements.append( elem1 )
        else:
          elem1 = symexpress3.SymNumber( 1, int( iPrime ), 1, 1, iCount, 1, 1 )
          # symDeno.add ( elem1 )
          symDeno.elements.append( elem1 )

      if lFoundOne == True:
        result = True
        # print( "symExpr   : {}".format( str( symExpr)))
        # print( "Fact   : {}".format( str( symFact )))
        # print( "symDeno: {}".format( str( symDeno )))

        if elem.factDenominator > 1 :
          elem1 = symexpress3.SymNumber( 1, 1, elem.factDenominator, 1, 1, 1 )
          # symDeno.add( elem1 )
          symDeno.elements.append( elem1 )

        symReplace = symexpress3.SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
        symReplace.add( symFact )
        if symDeno.numElements() > 0:
          symReplace.add( symDeno )

        # print( "fact old elem: {}".format( str( elem )))
        # print( "fact new elem: {}".format( str( symReplace)))

        symExpr.elements[ iCnt ] = symReplace

    # simplify the factDenominator
    # (1/27)^^(1/2) = (((1/3)^2)*3)^^(1/2) = 1/3 * 3^^(1/2)
    # for iCnt in range( 0, len( symExpr.elements )):
    for iCnt, elem in enumerate( symExpr.elements ):
      # elem = symExpr.elements[ iCnt ]

      # print( "check: {}".format( str( elem )))

      if not isinstance( elem, symexpress3.SymNumber ):
        continue
      if elem.onlyOneRoot != 1 :
        continue
      if elem.factSign != 1 :
        continue
      if elem.powerDenominator == 1 :
        continue
      if elem.factDenominator == 1 :
        continue

      # print( "check 2: deno:{}, elem: {}".format( elem.factDenominator, str( elem )))

      # symFact = SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
      # symDeno = SymExpress( '*', elem.powerSign, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)
      symFact = symexpress3.SymExpress( '*', 1, 1, 1, elem.onlyOneRoot )
      symDeno = symexpress3.SymExpress( '*', 1, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)

      lFoundOne = False
      dPrimeSet = primefactor.FactorizationDict( elem.factDenominator )

      # print ( "dPrimeSet factDenominator: {}".format( dPrimeSet ))
      for iPrime, iCount in dPrimeSet.items():
        # print( "iPrime: {}, iCount: {}, elem.powerDenominator: {}".format( iPrime, iCount,elem.powerDenominator ))
        if iCount >= elem.powerDenominator :
          iDenom    = iCount // elem.powerDenominator
          iRad      = iCount % elem.powerDenominator
          lFoundOne = True

          elem1 = symexpress3.SymNumber( 1, 1, int( iPrime ), 1, iDenom, 1, 1 )
          # symFact.add ( elem1 )
          symFact.elements.append ( elem1 )

          if iRad > 0 :
            elem1 = symexpress3.SymNumber( 1, 1, int( iPrime ), 1, iRad, 1, 1 )
            # symDeno.add ( elem1 )
            symDeno.elements.append( elem1 )
        else:
          elem1 = symexpress3.SymNumber( 1, 1, int( iPrime ), 1, iCount, 1, 1 )
          # symDeno.add ( elem1 )
          symDeno.elements.append( elem1 )

      if lFoundOne == True :
        result = True
        # print( "symExpr   : {}".format( str( symExpr)))
        # print( "Fact   : {}".format( str( symFact )))
        # print( "symDeno: {}".format( str( symDeno )))

        if elem.factCounter > 1 :
          elem1 = symexpress3.SymNumber( 1, elem.factCounter, 1, 1, 1, 1 )
          # symDeno.add( elem1 )
          symDeno.elements.append( elem1 )

        # symReplace = SymExpress( '*' )
        symReplace = symexpress3.SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )

        # symReplace.add( symFact )
        symReplace.elements.append( symFact )
        if symDeno.numElements() > 0:
          # symReplace.add( symDeno )
          symReplace.elements.append( symDeno )

        # print( "deno old elem: {}".format( str( elem )))
        # print( "deno new elem: {}".format( str( symReplace)))
        symExpr.elements[ iCnt ] = symReplace

    # eliminate the factDenominator
    # (1/3)^(1/2) = 3 * 3^(1/2)

    # cBefore = str( symExpr )
    # dBefore = symExpr.getValue()
    # for iCnt in range( 0, len( symExpr.elements )):
    for iCnt, elem in enumerate( symExpr.elements ):
      # elem = symExpr.elements[ iCnt ]

      # print( "check: {}".format( str( elem )))

      if not isinstance( elem, symexpress3.SymNumber ):
        continue
      if elem.onlyOneRoot != 1 :
        continue
      if elem.factSign != 1 :
        continue
      if elem.powerDenominator == 1 :
        continue
      if elem.factDenominator == 1 :
        continue

      elemnew = elem.copy()
      elemnew.factDenominator = 1
      elemnew.powerSign       = 1
      elemfact = symexpress3.SymNumber( 1, 1, elem.factDenominator, 1, 1, 1 )

      iFactCounter = elem.factCounter
      # print( "iFactCounter: {}".format( iFactCounter ))
      for iFact in range( 1, elem.powerDenominator ):
        iFactCounter *= elem.factDenominator
        # print( "iFactCounter: {} = {}".format( iFact, iFactCounter ))
      elemnew.factCounter = iFactCounter

      symReplace = symexpress3.SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
      # symReplace.add( elemfact )
      # symReplace.add( elemnew )
      symReplace.elements.append( elemfact )
      symReplace.elements.append( elemnew  )

      #dValueElem = elem.getValue()
      #dValueRep  = symReplace.getValue()
      #if ( dValueElem != dValueRep ):
      #  print( "quotation old elem: {} = {}".format( dValueElem, str( elem )))
      #  print( "quotation new elem: {} = {}".format( dValueRep , str( symReplace)))

      symExpr.elements[ iCnt ] = symReplace
      result = True

    #cAfter = str( symExpr )
    #dAfter = symExpr.getValue()
    #if ( True or dAfter != dBefore ):
    #   print( "quotation before: {} = {}".format( dBefore, cBefore))
    #   print( "quotation after : {} = {}".format( dAfter , cAfter ))
    return result


  def _expressOptimze( self, symExpr:symexpress3.SymExpress ) -> bool :
    # optimize expression (4   + 4 a  )^^(1/2) = 2  (1 + a)^^(1/2)
    #                     (1/4 + 1/4 a)^^(1/2) = 1/2(1 + a)^^(1/2)

    def _cleanup( arrElem:list[dict[int,int]] ) -> bool :
      powerSearch = symExpr.powerDenominator
      firstElem   = True
      allEmpty    = False
      tebeRemoved = []
      for dPrimeSet in arrElem:
        # print( "Check: " + str( dPrimeSet ))
        if firstElem == True:
          firstElem = False
          if len( dPrimeSet ) == 0:  # pylint: disable=simplifiable-if-statement
            allEmpty = True
          else:
            allEmpty = False
        else:
          if len( dPrimeSet ) == 0:
            if allEmpty == False:
              return False
          else:
            if allEmpty == True:
              return False

        if allEmpty == False:
          # delete all power lower then powerSearch
          removeNumber = []
          for iPrime, iCount in dPrimeSet.items():
            if iCount < powerSearch:
              # del dPrimeSet[ iPrime ]
              removeNumber.append( iPrime )
            else:
              if iCount % powerSearch != 0:
                dPrimeSet[ iPrime ] = (iCount // powerSearch) * powerSearch
          for iRem in removeNumber:
            del dPrimeSet[ iRem ]
          if len( dPrimeSet ) == 0:
            return False
        else:
          # print( "Remove" )
          # arrElem.remove( dPrimeSet )
          tebeRemoved.append( dPrimeSet )

      for delElem in tebeRemoved:
        arrElem.remove( delElem )

      return True

    def _lowestPower( elemArr:list[dict[int,int]] ) -> bool :

      if len( elemArr ) == 0:
        return True

      setPrimes = None
      for dPrimeSet in elemArr:
        if setPrimes == None:
          setPrimes = dPrimeSet
        else:
          newSet = {}
          for iPrime, iCount in setPrimes.items():
            if iPrime in dPrimeSet:
              newSet[ iPrime ] = min( iCount, dPrimeSet[ iPrime ] )
          setPrimes = newSet

      if setPrimes == None:
        return False

      if len( setPrimes ) == 0:
        return False

      # print( f"New prime set: {setPrimes}")
      elemArr.clear()
      elemArr.append( setPrimes )

      # print( f"elemArr prime set: {elemArr}")

      return True

    def _negativeRoot( symExpr:symexpress3.SymExpress ) -> bool :
      # search of negative number in * expression by principal root 1/2
      # ( -30)^^(1/2) -> i (30)^^(1/2)
      if symExpr.symType == '*' and symExpr.onlyOneRoot == 1 and symExpr.powerCounter == 1 and symExpr.powerDenominator == 2:
        foundNegative = 0
        for elemCheck in symExpr.elements:
          if isinstance( elemCheck, symexpress3.SymNumber ) and elemCheck.factSign == -1 and elemCheck.power == 1:
            foundNegative += 1
        if foundNegative == 1:
          # ok replace expression
          symCopy           = symExpr.copy()
          symCopy.elements.append ( symexpress3.SymNumber( -1, 1, 1,1 )) # -1
          symCopy.powerSign = 1

          symExpr.powerCounter     = 1
          symExpr.powerDenominator = 1 # do not change power sign
          symExpr.elements         = []
          symExpr.elements.append( symexpress3.SymVariable( 'i' ))
          symExpr.elements.append( symCopy )

          return True

      return False


    result = False

    # print( "Start: " + str( symExpr ))

    if not isinstance( symExpr, symexpress3.SymExpress):
      return result

    # print( "Start 2: " + str( symExpr ))

    if symExpr.powerDenominator == 1:
      # print( "symexpress: " + str( symExpr ) )
      # symexpress3.SymExpressTree( symExpr )
      return result

    # print( "Start 3: " + str( symExpr ))

    # print( "Start 3 symExpr.onlyOneRoot: " + str( symExpr.onlyOneRoot ))

    # if symExpr.onlyOneRoot != 1:
    #   return result

    # print( "Start 4: " + str( symExpr ))

    # if symExpr.powerSign == -1:
    #  # print( f"power negative {str(symExpr)}")
    #  result = _negativeRoot( symExpr )
    #  # print( f"Result: {result} : {str(symExpr)}")
    #  return result
    #  # return result

    # print( "Start 5: " + str( symExpr ))

    # if this exist do nothing, first multiply
    # 25 * 257 * 5^^-1
    if symExpr.symType == '*':
      iFoudnNumbers = 0
      for elem in symExpr.elements :
        if elem.powerDenominator > 1:
          continue
        if elem.powerCounter > 1:
          continue
        if not isinstance( elem, symexpress3.SymNumber)  :
          continue
        iFoudnNumbers += 1
        if iFoudnNumbers > 1:
          break

      if iFoudnNumbers > 1:
        return result

    # print(" Start _expressOptimze" )

    # minNumber = 2 ** symExpr.powerDenominator  # min number 2^denominator, 2^2 = 4, 2^3 = 6
    arrFact  :list[dict[int,int]]= []
    arrDenom :list[dict[int,int]]= []
    found    = False
    if symExpr.symType == '*' :
      # search for first SymNumber with power of 1
      # get factCounter
      # get factDenominator
      found = False
      for elem in symExpr.elements :
        if not isinstance( elem, symexpress3.SymNumber ):
          continue
        # no powers
        if elem.powerIsOne() == False :
          continue
        dPrimeSet = primefactor.FactorizationDict( elem.factCounter )
        arrFact.append( dPrimeSet )

        dPrimeSet = primefactor.FactorizationDict( elem.factDenominator )
        arrDenom.append( dPrimeSet )

        found = True
        # only 1 number supported
        break

      if found == False:
        # print( "Number invalid: " + str( symExpr ))
        return result

    else:
      # search in each element for a SymNumber with power of 1
      # get factCounter
      # get factDenominator
      found = False

      # print( "check onlyoneroot plus: " + str( symExpr ))

      for elemplus in symExpr.elements:
        if isinstance( elemplus, symexpress3.SymNumber ):
          if elemplus.powerIsOne() == False:
            # print( "Power - 1 not 1: " + str( elemplus ))
            return result

          dPrimeSet = primefactor.FactorizationDict( elemplus.factCounter )
          arrFact.append( dPrimeSet )

          dPrimeSet = primefactor.FactorizationDict( elemplus.factDenominator )
          arrDenom.append( dPrimeSet )

        elif isinstance( elemplus, symexpress3.SymExpress ):
          if elemplus.powerIsOne() == False :
            # print( "Power - 2 not 1: " + str( elemplus ))
            return result

          if elemplus.symType == '+' and elemplus.numElements() != 1:
            # print( "num elements not 1: " + str( elemplus ))
            return result

          found = False
          for elem in elemplus.elements:
            # print( "Check : " + str( elem ) + str( type( elem )))
            if elem.powerIsOne() == False :
              continue
            if not isinstance( elem, symexpress3.SymNumber ):
              continue
            # no powers
            dPrimeSet = primefactor.FactorizationDict( elem.factCounter )
            arrFact.append( dPrimeSet )

            dPrimeSet = primefactor.FactorizationDict( elem.factDenominator )
            arrDenom.append( dPrimeSet )

            found = True
            # only 1 number supported
            break
          if found == False:
            # print( "Nothing found" )
            return result

        else:
          # print( "Not supported type" )
          return result # only numbers and symexpress supported

    # print( "Found: " + str( found ))

    if found == False:
      return result

    # print( "arrFact : " + str( arrFact  ))
    # print( "arrDemon: " + str( arrDenom ))

    # check if the powers are greater of equal expression power
    if _cleanup( arrFact  ) != True:
      arrFact = []
      # return False

    # print( "check 2" )

    if _cleanup( arrDenom ) != True:
      arrDenom = []
      # return False

    # print( "check 3" )

    if len( arrFact ) == 0 and len( arrDenom ) == 0:
      # print( "Noting to do")
      return _negativeRoot( symExpr )
      # return False

    # print( "arrFact 2: " + str( arrFact  ))
    # print( "arrDemon2: " + str( arrDenom ))

    # check all the bases and powers must be equal
    if _lowestPower( arrFact ) != True:
      return False

    if _lowestPower( arrDenom ) != True:
      return False

    # print( "arrFact 3: " + str( arrFact  ))
    # print( "arrDemon3: " + str( arrDenom ))

    if len( arrFact ) == 0 and len( arrDenom ) == 0:
      return False

    # make number (common factor)
    symNum = symexpress3.SymExpress( '*' )
    if len( arrFact ) > 0:
      # all powers are now the same
      for iPrime, iCount in arrFact[ 0 ].items():
        newNum = symexpress3.SymNumber()
        newNum.factCounter   = iPrime
        newNum.powerCounter  = iCount
        symNum.elements.append( newNum )

    if len( arrDenom ) > 0:
      # all powers are now the same
      for iPrime, iCount in arrDenom[ 0 ].items():
        newNum = symexpress3.SymNumber()
        newNum.factDenominator = iPrime
        newNum.powerCounter    = iCount
        symNum.elements.append( newNum )

    # print( "Common factor: " + str( symNum ))

    # copy symExpr
    copySymExpr = symExpr.copy()
    orgPowerCounter = copySymExpr.powerCounter

    # print( "powercounter: " + str( copySymExpr.powerCounter ))

    # create new SymExpress = *
    newSymExpr = symexpress3.SymExpress( '*' )
    # copy the power from symExpr to new
    newSymExpr.powerCounter     = symExpr.powerCounter
    newSymExpr.powerDenominator = symExpr.powerDenominator
    newSymExpr.powerSign        = symExpr.powerSign
    newSymExpr.onlyOneRoot      = symExpr.onlyOneRoot
    # set power of copy symExpress to 1
    copySymExpr.powerCounter     = 1
    copySymExpr.powerDenominator = 1
    copySymExpr.powerSign        = 1
    # add copy to new
    newSymExpr.elements.append( copySymExpr )
    # add 1/fact to new
    # add 1/denom to new
    symNum.powerSign = -1
    newSymExpr.add( symNum )
    symNum.powerSign = 1

    # set org symexpres powerFactor & powerDenomotor to 1 (not sign)
    symExpr.powerCounter     = 1
    symExpr.powerDenominator = 1
    # make org empty
    symExpr.elements = []
    # set org to *
    symExpr.symType = '*'
    # add radical of fact
    # add radical of denom
    symNum.powerDenominator = newSymExpr.powerDenominator

    # print( "symNum 1: " + str( symNum ))

    symNum1 = symexpress3.SymExpress( '*' )
    symNum1.powerSign = symExpr.powerSign # set correct power sign

    symNum1.add( symNum )
    symNum1.powerCounter = orgPowerCounter

    # print( "symNum 1a: " + str( symNum1 ))

    # want whole number
    # otherwise optimize 'multiply' will put the radicals together (circle)
    symNum1.optimize()
    symNum1.optimize( "multiply" )
    symNum1.optimize()
    symNum1.optimize( "power" )
    symNum1.optimize()

    self._numberOptimize( symNum1 )  # should be optimizeNumberOnlyOneRoot but that gives a circle too...
    symNum1.optimize()
    self._numberOptimize( symNum1 )
    symNum1.optimize()

    # print( "symNum 2: " + str( symNum ))


    # print( " " )
    # symexpress3.SymExpressTree( symNum1 )

    # print( " " )
    # print( "symNum optimized: " + str( symNum1 ))
    # print( " " )


    # symExpr.add( symNum1 )
    symExpr.elements.append( symNum1 )
    # add new to org
    # symExpr.add( newSymExpr )
    symExpr.elements.append( newSymExpr )
    symExpr.powerSign = 1 # correct powersign

    # print( "New symexpress: " + str( symExpr ))

    result = True

    return result

  def optimize( self, symExpr:symexpress3.TypVarSym3Object, action:None|str ) -> bool:

    result = False
    if self.checkExpression( symExpr, action ) != True:
      # print( "Afgekeurd: " + symExpr.symType )
      return result

    # set type for mypy
    # https://mypy.readthedocs.io/en/stable/type_narrowing.html
    symExpr = typing.cast( symexpress3.SymExpress, symExpr )

    # result |= self._numberOptimize( symExpr )
    # if result == True:
    #   return result

    # print( "Start OnleOneRoot: " + str( symExpr ) )

    # not wanted to get all the factors out of the radical
    result |= self._expressOptimze( symExpr )
    # if result == True:
    #   return result

    return result


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None:
  """
  Unit test
  """
  def _Check( testClass :OptimizeOnlyOneRoot
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

  testClass = OptimizeOnlyOneRoot()

  symTest:symexpress3.TypVarSym3Object = symexpress3.SymFormulaParser( '(2315819305000550693112168347915158822781184016504196548362331 + 1127493071704679652558486495801124357814515802175332688 * 2^^(1/2) )^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = typing.cast( symexpress3.SymExpress, symTest ) # special for mypy
  symTest = symTest.elements [ 0 ]
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  # big numbers are disabled for speed
  # _Check( testClass, symOrg, symTest, "255107^^4 * ((2315819305000550693112168347915158822781184016504196548362331 + 1127493071704679652558486495801124357814515802175332688 * 2^^(1/2)) * (255107^^8)^^-1)^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( '(4 + 8 a)^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = symTest.elements [ 0 ]
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "2 * ((4 + 8 * a) * (2^^2)^^-1)^^(1/2)" )

  symTest = symexpress3.SymFormulaParser( '(1/4 + 1/8 a)^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = symTest.elements [ 0 ]
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "(1/2) * (((1/4) + (1/8) * a) * ((1/2)^^2)^^-1)^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( '(4/27 + 8/9 a)^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = symTest.elements [ 0 ]
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "2 * (1/3) * (((4/27) + (8/9) * a) * (2^^2 * (1/3)^^2)^^-1)^^(1/2)" )



  symTest = symexpress3.SymFormulaParser( '(-1 * 5 * 6^^(1/3) )^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = symTest.elements [ 0 ]
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "i * ((-5) * 6^^(1/3) * (-1))^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( '(-1 * 5 * 6^^(1/3) )^^(-1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = symTest.elements [ 0 ]
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "(i * ((-5) * 6^^(1/3) * (-1))^^(1/2))^^-1" )


if __name__ == '__main__':
  Test( True )
