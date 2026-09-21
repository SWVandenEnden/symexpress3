#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Multiply for Sym Express 3

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

class OptimizeMultiply( optimizeBase.OptimizeBase ):
  """
  Multiply the elements of this expressions and his sub-expressions
  \n(x+1)(x+1) becomes x^2 + 2x + 1
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "multiply"
    self._symtype      = "*"
    self._desc         = "Multiply elements"


  def optimize( self, symExpr:symexpress3.TypVarSym3Object, action:None|str ) -> bool:

    result = False

    if self.checkExpression( symExpr, action ) != True:
      return result

    symExpr = typing.cast( symexpress3.SymExpress, symExpr )


    # multiply symNumbers
    def _multiplyNumbers() -> bool :

      result = False

      if symExpr.symType != '*':
        return result

      elem = None
      iCnt = 0

      for iCnt, elem in enumerate( symExpr.elements ) :
        if elem.powerDenominator != 1:
          continue
        if not isinstance( elem, symexpress3.SymNumber ):
          continue
        break

      if elem == None:
        return result

      elem = typing.cast( symexpress3.SymNumber, elem )

      # print( "_multiplyNumbers start: {}".format( symExpr ) )

      for iCnt2 in range( len( symExpr.elements ) -1 , -1, -1 ) :

        if iCnt2 <= iCnt:
          break

        elem2 = symExpr.elements[ iCnt2 ]

        if elem2.powerDenominator > 1:
          continue

        if not isinstance( elem2, symexpress3.SymNumber ):
          continue

        if elem2.powerCounter > 1:
          elem2.factCounter     = pow( elem2.factCounter * elem2.factSign, elem2.powerCounter )
          elem2.factDenominator = pow( elem2.factDenominator             , elem2.powerCounter )

        if elem.powerCounter > 1:
          elem.factCounter     = pow( elem.factCounter * elem.factSign, elem.powerCounter )
          elem.factDenominator = pow( elem.factDenominator            , elem.powerCounter )
          elem.powerCounter    = 1

        if elem2.powerSign != elem.powerSign:
          elem.factDenominator *= elem2.factCounter
          elem.factCounter     *= elem2.factDenominator
        else:
          elem.factCounter     *= elem2.factCounter
          elem.factDenominator *= elem2.factDenominator

        elem.factSign    *= elem2.factSign
        # elem.onlyOneRoot  = max( elem.onlyOneRoot, elem2.onlyOneRoot )
        elem.onlyOneRoot  = min( elem.onlyOneRoot, elem2.onlyOneRoot )

        del symExpr.elements[ iCnt2 ]
        result = True

      return result

    # get all sub expressions with power of 1
    def _multiplyElemGetSubPowerOne() -> bool :
      result = False

      if symExpr.symType != '*':
        return result

      iStart = 0
      lFound = True

      while lFound == True :

        lFound  = False
        iMaxLen = len( symExpr.elements )

        for iCnt in range( iStart, iMaxLen ):

          elem1 = symExpr.elements[ iCnt ]

          if elem1.powerIsOne() == False:
            continue

          if not isinstance( elem1, symexpress3.SymExpress ):
            continue

          if elem1.symType != '*':
            continue

          lFound = True
          for elem2 in elem1.elements :
            symExpr.elements.append( elem2 )

          del symExpr.elements[ iCnt ]
          iStart = iCnt
          result = True

          break

      return result

    # multiply SymVariable with expression of type +
    def _multiplyElemUnitExpress() -> bool :
      result = False
      if symExpr.symType != '*':
        return result

      # print ( "_multiplyElemUnitExpress start")

      lFound = True
      while( lFound == True and len( symExpr.elements ) > 1 ):
        # print ( f"_multiplyElemUnitExpress: {len( symExpr.elements )}")
        lFound = False
        iCnt   = 0
        for iCnt, elem1 in enumerate( symExpr.elements ) :

          # a root have multiple solutions, cannot multiply with + expressions
          if (elem1.powerDenominator > 1 and elem1.onlyOneRoot == 0 ):
            continue

          if not isinstance( elem1, symexpress3.SymVariable ):
            continue

          iCnt2 = 0
          while( lFound == False and iCnt2 < len( symExpr.elements )):
            if iCnt == iCnt2:
              iCnt2 += 1
              continue
            elem2  = symExpr.elements[ iCnt2 ]
            iCnt2 += 1

            if not isinstance( elem2, symexpress3.SymExpress ):
              continue

            # only multiply no + expressions
            if elem2.symType != '+' :
              continue

            # only power of 1 is supported or same powers (numbers of roots must be the same)
            # if (elem2.power == 1 or ( elem2.power == elem1.power and ( elem1.powerDenominator == 1 or elem1.onlyOneRoot == elem2.onlyOneRoot ) ) ):
            if (elem2.powerIsOne() == True or ( elem2.power == elem1.power and ( elem1.powerDenominator == 1 or elem1.onlyOneRoot == elem2.onlyOneRoot ) ) ):
              pass
            else:
              continue

            # found one
            # delete elements from current expression
            if iCnt < iCnt2:
              del symExpr.elements[ iCnt2 - 1 ] # already has done +1
              del symExpr.elements[ iCnt      ]
            else:
              del symExpr.elements[ iCnt      ]
              del symExpr.elements[ iCnt2 - 1 ] # already has done +1

            lFound = True
            result = True

            elemnew = symexpress3.SymExpress( '+' )
            if elem1.power == elem2.power:
              elemnew.powerSign        = elem1.powerSign
              elemnew.powerCounter     = elem1.powerCounter
              elemnew.powerDenominator = elem1.powerDenominator
              elemnew.onlyOneRoot      = elem1.onlyOneRoot

              elem1.powerSign        = 1
              elem1.powerCounter     = 1
              elem1.powerDenominator = 1

            for iCntSub1 in range( 0, elem2.numElements() ) :
              elem3    = elem2.elements[ iCntSub1 ]
              elemnew2 = symexpress3.SymExpress( '*' )
              elemnew2.elements.append( elem1 )
              elemnew2.elements.append( elem3 )
              elemnew.elements.append( elemnew2 )

            symExpr.add( elemnew )
            # symExpr.elements.append( elemnew ) -> Cannot do this. Elements out out symExpr are all ready append. see few lines above

          if lFound == True:
            # print( f"_multiplyElemUnitExpress found one: {str(symExpr)}")
            break

      # print ( "_multiplyElemUnitExpress end")
      return result

    # multiply 2 expressions
    def _multiplyElemExpressExpress() -> bool :
      result = False
      if symExpr.symType != '*':
        return result

      maxLen = len( symExpr.elements )
      if maxLen <= 1 :
        return result

      # print ( "_multiplyElemExpressExpress start")
      arrDel:set[int]  = set()
      # arrSkip:set[int] = set()
      arrValid:set[int]= set()


      # print ( f'_multiplyElemExpressExpress elements count: {len( symExpr.elements )}   ' )
      for iCnt, elem1 in enumerate( symExpr.elements ) :

        # only multiply with power of 1
        if elem1.powerIsOneOrMinusOne() == False:
          # arrSkip.add( iCnt )
          continue

        # only multiple expressions
        if not isinstance( elem1 , symexpress3.SymExpress ):
          # arrSkip.add( iCnt )
          continue

        if elem1.symType != '+':
          # arrSkip.add( iCnt )
          continue


        arrValid.add( iCnt )


      # nothing to do
      if len( arrValid ) <= 1 :
        return result

      # maxLen1 = maxLen - 1
      # maxLen2 = maxLen
      # for iCnt in range( 0, maxLen1 ) :
      for iCnt in arrValid :

        # if iCnt in arrSkip:
        #   continue

        if iCnt in arrDel:
          continue

        elem1 = symExpr.elements[ iCnt ]

        # fncFilter = lambda x: x > iCnt

        # for iCnt2 in range( iCnt + 1, maxLen2 ) :
        subSet = { x for x in arrValid if x > iCnt and x not in arrDel }
        for iCnt2 in subSet :
        # for iCnt2 in arrValid  :
        # for iCnt2 in filter( lambda x:x > iCnt, arrValid ):
        # for iCnt2 in filter( fncFilter, arrValid ):

          # if iCnt2 in arrSkip:
          # if iCnt2 not in arrValid:
          # if iCnt2 <= iCnt:
          #   continue

          # the set has no fixed order
          # if iCnt2 in arrDel:
          #   continue

          elem2 = symExpr.elements[ iCnt2 ]

          if elem2.powerSign != elem1.powerSign:
            continue

          # 2 plus expression with power of 1
          # the factors are already one, see loops above
          elemnew           = symexpress3.SymExpress( '+' )
          elemnew.powerSign = elem2.powerSign

          # print ( f'_multiplyElemExpressExpress elem1: {len( elem1.elements )}, elem2: {len(elem2.elements)}' )

          # strSymExpr = str( symExpr )
          # if len( strSymExpr ) > 500000000:
          #   import pudb; pudb.set_trace()
          #  with open("formula_big.txt", mode="w", encoding="utf-8") as f:
          #    f.write(strSymExpr)
          #  with open("formula_elem1.txt", mode="w", encoding="utf-8") as f:
          #    f.write( str(elem1) )
          #  with open("formula_elem2.txt", mode="w", encoding="utf-8") as f:
          #    f.write( str(elem2) )

          elem1 = typing.cast( symexpress3.SymExpress, elem1 )
          elem2 = typing.cast( symexpress3.SymExpress, elem2 )

          for elemSub1 in elem1.elements:

            for elemSub2 in elem2.elements:
              elem12 = symexpress3.SymExpress( '*' )
              elem12.elements.append( elemSub1 )
              elem12.elements.append( elemSub2 )
              elemnew.add( elem12 )

          # elemnew.optimizeNormal( extra=['nodebug'] ) # make's it smaller but is this wise on this level
          elemnew.optimize( "multiply" ) # this is faster but cost more memory
          elemnew.optimize( "add"      )
          elemnew.optimize( None       )

          symExpr.elements[ iCnt ] = elemnew

          arrDel.add( iCnt2 )
          elem1  = symExpr.elements[ iCnt ]
          result = True

      # print ( f"_multiplyElemExpressExpress end: {result}")

      # del elements
      for iCnt in sorted( arrDel, reverse=True):
        del symExpr.elements[ iCnt ]

      return result

    # multiply 2 variables
    def _multiplyElemVarVar() -> bool :
      result = False

      if symExpr.symType != '*':
        return result

      maxLen = len( symExpr.elements )

      if maxLen <= 1:
        return result

      arrDel:set[int]  = set()
      # arrSkip:set[int] = set()
      arrValid:set[int]= set()

      for iCnt, elemskip in enumerate( symExpr.elements ) :
        if not isinstance( elemskip, symexpress3.SymVariable ):
          # arrSkip.add( iCnt )
          continue
        arrValid.add( iCnt )

      # no variables found
      # if len( arrSkip ) + 1 >= maxLen :
      if len( arrValid ) <= 1:
        return result

      # multiple all units with same name
      # maxLen1 = maxLen - 1
      # maxLen2 = maxLen

      # for iCnt in range( 0, maxLen1 ) :
      for iCnt in arrValid :

        # if iCnt in arrSkip:
        #   continue

        if iCnt in arrDel:
          continue

        elem1 = typing.cast( symexpress3.SymVariable, symExpr.elements[ iCnt ] )

        # for iCnt2 in range( iCnt + 1, maxLen2 ) :
        subSet = { x for x in arrValid if x > iCnt and x not in arrDel }
        for iCnt2 in subSet :

        # for iCnt2 in arrValid:
        # for iCnt2 in filter( lambda x:x > iCnt, arrValid ):

          # if iCnt2 in arrSkip:
          # if iCnt2 not in arrValid:
          # if iCnt2 <= iCnt:
          #   continue

          # if iCnt2 in arrDel:
          #   continue

          elem2 = typing.cast( symexpress3.SymVariable, symExpr.elements[ iCnt2 ] )

          # it must have the same name
          if elem2.name != elem1.name:
            continue

          # Special case for infinity
          # If power sign is not the same then do nothing
          # infinity * infinity / infinity = infinity / infinity = 1
          # see optimzeInfinity.py & optSymVariableInfinity.py
          if elem1.name == "infinity" and elem1.powerSign != elem2.powerSign:
            continue

          rememberPowerDenominator = elem1.powerDenominator

          # if it is a fraction, make the denominator equal
          elem1.powerCounter     *= elem2.powerDenominator
          elem1.powerDenominator *= elem2.powerDenominator

          elem2.powerCounter     *= rememberPowerDenominator # elemnew.powerDenominator
          elem2.powerDenominator *= rememberPowerDenominator # elemnew.powerDenominator

          iCounter = elem1.powerCounter * elem1.powerSign + elem2.powerCounter * elem2.powerSign

          elem1.powerSign    = 1
          elem1.powerCounter = iCounter
          elem1.onlyOneRoot  = min( elem1.onlyOneRoot, elem2.onlyOneRoot )

          arrDel.add( iCnt2 )
          elem1  = typing.cast( symexpress3.SymVariable, symExpr.elements[ iCnt ] )

          result = True

      # del elements
      for iCnt in sorted( arrDel, reverse=True):
        del symExpr.elements[ iCnt ]

      return result

    # multiply number with multiple-plus-expression
    def _multiplyNumberExpress() -> bool :
      result = False
      if symExpr.symType != '*':
        return result

      if symExpr.numElements() != 2:
        return result

      elem1 = symExpr.elements[ 0 ]
      elem2 = symExpr.elements[ 1 ]

      elemNum  = None
      elemExpr = None

      if isinstance( elem1, symexpress3.SymNumber ):
        elemNum = elem1
      elif isinstance( elem2, symexpress3.SymNumber ):
        elemNum = elem2
      if elemNum == None:
        return result

      if isinstance( elem1, symexpress3.SymExpress ):
        elemExpr = elem1
      elif isinstance( elem2, symexpress3.SymExpress ):
        elemExpr = elem2
      if elemExpr == None:
        return result

      if elemExpr.symType != '+':
        return result
      if elemExpr.powerIsOne() == False :
        return result

      symExpr.elements = []
      symExpr.symType  = '+'
      result           = True
      for elemsub in elemExpr.elements :
        elemnew = symexpress3.SymExpress( '*' )
        elemnew.add( elemNum )
        elemnew.elements.append( elemsub )

        symExpr.elements.append( elemnew )

      return result

    # multiply plus-expression with multiply-expression
    def _multplyPlusExpressMultiply() -> bool :
      result = False
      if symExpr.symType != '*':
        return result

      maxLen = symExpr.numElements()

      if maxLen <= 1:
        return result

      for iCnt, elem in enumerate( symExpr.elements ) :
        elem = symExpr.elements[ iCnt ]

        if elem.powerIsOne() == False :
          continue

        if not isinstance( elem, symexpress3.SymExpress ):
          continue
        if elem.symType != '+':
          continue
        if elem.numElements() <= 1:
          continue
        # found a plus expression within a multiply express
        # make it a plus expression
        symMulti = symexpress3.SymExpress( '*' )
        for iCnt2, elemSub2 in enumerate( symExpr.elements ):
          if iCnt2 == iCnt:
            continue
          symMulti.elements.append( elemSub2 )

        # print( 'SymMulti: {}'.format( str( SymMulti )))

        # if symMulti.numElements() == 0:
        if not symMulti.elements:
          continue

        # import pudb; pudb.set_trace()

        symExpr.symType  = '+'
        symExpr.elements = []
        result           = True
        for elemSub2 in elem.elements :
          symNew = symexpress3.SymExpress( '*' )
          symNew.add( symMulti )
          symNew.elements.append( elemSub2 )

          symExpr.elements.append( symNew )

        # SymExpress is now a plus expression
        return result

      return result

    # multiply radicals with the same base (onlyOneRoot only)
    def _multplyPlusMultiplyOnlyRoots() -> bool :
      result = False
      if symExpr.symType != '*':
        return result

      maxLen = len( symExpr.elements )

      if maxLen <= 1 :
        return result

      arrDel:set[int]  = set()
      # arrSkip:set[int] = set()
      arrValid:set[int]= set()


      for iCnt, elemskip in enumerate( symExpr.elements ) :
        if elemskip.powerDenominator == 1:
          # arrSkip.add( iCnt )
          continue

        if elemskip.onlyOneRoot == 0:
          # arrSkip.add( iCnt )
          continue

        arrValid.add( iCnt )

      # nothing found
      # if len( arrSkip ) + 1 >= maxLen :
      if len( arrValid ) <= 1:
        return result

      # maxLen1 = maxLen - 1
      # maxLen2 = maxLen

      # for iCnt in range( 0, maxLen1 ) :
      for iCnt in arrValid :

        # if iCnt in arrSkip:
        #   continue

        if iCnt in arrDel:
          continue

        elem = symExpr.elements[ iCnt ]

        # search for the next element with the same base
        subSet = { x for x in arrValid if x > iCnt and x not in arrDel }
        for iCnt2 in subSet :

        # for iCnt2 in range( iCnt + 1, maxLen2 ) :
        # for iCnt2 in arrValid:
        # for iCnt2 in filter( lambda x:x > iCnt, arrValid ):

          # if iCnt2 in arrSkip:
          # if iCnt2 not in arrValid:
          # if iCnt2 <= iCnt:
          #   continue

          # if iCnt2 in arrDel:
          #   continue

          elem2 = symExpr.elements[ iCnt2 ]

          if not elem.isEqual( elem2, True, False ):
            lOk = False

            # needed this 4 variable to initialize, but the initialize value is never used (pylint)
            rem1FactCounter   = 1
            rem2FactCounter   = 1
            rem1PowerCounter  = 1
            rem2PowerCounter  = 1

            if ( isinstance( elem, symexpress3.SymNumber ) and isinstance( elem2, symexpress3.SymNumber )):
              dPrimeSet1 = primefactor.FactorizationDict( elem.factCounter  )
              dPrimeSet2 = primefactor.FactorizationDict( elem2.factCounter )

              # print ( "dPrimeSet1: {}".format( dPrimeSet1 ))
              # print ( "dPrimeSet2: {}".format( dPrimeSet2 ))

              if ( len( dPrimeSet1 ) == 1 and len( dPrimeSet2 ) == 1 ):
                if list( dPrimeSet1.keys() )[0] == list( dPrimeSet2.keys() )[0] :
                  # 2 elements with the same base
                  # put the numbers in the counters of the power
                  # print( "list( dPrimeSet1)[ 0 ]: {}".format( list( dPrimeSet1.values())[ 0 ] ))
                  # print( "list( dPrimeSet2)[ 0 ]: {}".format( list( dPrimeSet2.values() )[ 0 ] ))

                  # not a nice solution but for the moment
                  elemcheck1 = elem.copy()
                  elemcheck1.powerSign        = 1
                  elemcheck1.powerDenominator = 1
                  elemcheck1.powerCounter     = 1

                  elemcheck2 = elem2.copy()
                  elemcheck2.powerSign        = 1
                  elemcheck2.powerDenominator = 1
                  elemcheck2.powerCounter     = 1

                  rem1FactCounter    = list( dPrimeSet1.keys()  )[ 0 ]
                  rem2FactCounter    = list( dPrimeSet2.keys()  )[ 0 ]
                  rem1PowerCounter  = elem.powerCounter  * list( dPrimeSet1.values())[ 0 ]
                  rem2PowerCounter  = elem2.powerCounter * list( dPrimeSet2.values())[ 0 ]

                  lOk = True

            if lOk == False:
              continue

            elemcheck1.factCounter   = rem1FactCounter
            elemcheck2.factCounter   = rem2FactCounter
            elemcheck1.powerCounter  = rem1PowerCounter
            elemcheck2.powerCounter  = rem2PowerCounter

            elemcheck1.powerSign        = 1
            elemcheck1.powerDenominator = 1
            elemcheck1.powerCounter     = 1

            elemcheck2.powerSign        = 1
            elemcheck2.powerDenominator = 1
            elemcheck2.powerCounter     = 1

            if not elemcheck1.isEqual( elemcheck2 ):
              continue

            elem  = typing.cast( symexpress3.SymNumber, elem  )
            elem2 = typing.cast( symexpress3.SymNumber, elem2 )

            elem.factCounter    = rem1FactCounter
            elem2.factCounter   = rem2FactCounter
            elem.powerCounter   = rem1PowerCounter
            elem2.powerCounter  = rem2PowerCounter

          # 2 radicals with the same denominator
          # add the powers
          if elem.powerDenominator != elem2.powerDenominator:

            # iPowerCounter1       = elem.powerCounter
            iPowerDenominator1   = elem.powerDenominator

            elem.powerDenominator  *= elem2.powerDenominator
            elem.powerCounter      *= elem2.powerDenominator

            elem2.powerCounter     *= iPowerDenominator1
            elem2.powerDenominator *= iPowerDenominator1

          iCounter = elem.powerCounter * elem.powerSign + elem2.powerCounter * elem2.powerSign

          elem.powerSign     = 1
          elem.powerCounter  = iCounter

          arrDel.add( iCnt2 )
          elem = symExpr.elements[ iCnt ]

          result = True

      # del elements
      for iCnt in sorted( arrDel, reverse=True):
        del symExpr.elements[ iCnt ]

      return result

    # multiply radicals with the same power
    def _multplyRadicalsSamePowerOnlyRoots() -> bool :
      result = False

      if symExpr.symType != '*':
        return result

      maxLen = len( symExpr.elements )

      if maxLen <= 1 :
        return result

      arrDel:set[int]  = set()
      # arrSkip:set[int] = set()
      arrValid:set[int]= set()

      for iCnt, elemskip in enumerate( symExpr.elements ) :
        if elemskip.powerDenominator == 1:
          # arrSkip.add( iCnt )
          continue
        if elemskip.onlyOneRoot == 0 :
          # arrSkip.add( iCnt )
          continue

        arrValid.add( iCnt )

      # nothing found
      # if len( arrSkip ) + 1 >= maxLen :
      if len( arrValid ) <= 1:
        return result

      # maxLen1 = maxLen - 1
      # maxLen2 = maxLen

      # for iCnt in range( 0, maxLen1 ) :
      for iCnt in arrValid :
        oExpr  = None

        # if iCnt in arrSkip:
        #   continue

        if iCnt in arrDel:
          continue

        elem = symExpr.elements[ iCnt ]

        subSet = { x for x in arrValid if x > iCnt and x not in arrDel }
        for iCnt2 in subSet :
        # for iCnt2 in range( iCnt + 1, maxLen2 ) :
        # for iCnt2 in arrValid:

          # if iCnt2 in arrSkip:
          # if iCnt2 not in arrValid:
          # if iCnt2 <= iCnt:
          #   continue

          # if iCnt2 in arrDel:
          #   continue

          elem2 = symExpr.elements[ iCnt2 ]

          if (   elem2.powerSign        != elem.powerSign
              or elem2.powerCounter     != elem.powerCounter
              or elem2.powerDenominator != elem.powerDenominator
            ):
            continue

          if oExpr == None:
            oExpr = symexpress3.SymExpress( '*' )
            oExpr.powerSign        = elem.powerSign
            oExpr.powerCounter     = elem.powerCounter
            oExpr.powerDenominator = elem.powerDenominator
            oExpr.onlyOneRoot      = 1

          elem2.powerSign        = 1
          elem2.powerCounter     = 1
          elem2.powerDenominator = 1

          oExpr.elements.append( elem2 )

          arrDel.add( iCnt2 )

        # if lFound == True:
        if oExpr != None:

          elem.powerSign        = 1
          elem.powerCounter     = 1
          elem.powerDenominator = 1

          oExpr.elements.append( elem )
          symExpr.elements[ iCnt ] = oExpr

          result = True

      # del elements
      for iCnt in sorted( arrDel, reverse=True):
        del symExpr.elements[ iCnt ]

      # print( "symExpr: {}".format( str( symExpr )) )
      return result

    def _multiplyFunctionFunction() -> bool :
      result = False

      if symExpr.symType != '*':
        return result

      maxLen = len( symExpr.elements )

      if maxLen <= 1 :
        return result

      arrDel:set[int]  = set()
      # arrSkip:set[int] = set()
      arrValid:set[int]= set()


      for iCnt, elemskip in enumerate( symExpr.elements ) :
        if not isinstance( elemskip, symexpress3.SymFunction ):
          # arrSkip.add( iCnt )
          continue

        if elemskip.onlyOneRoot == 0 :
          # arrSkip.add( iCnt )
          continue

        arrValid.add( iCnt )


      # nothing found
      # if len( arrSkip ) + 1 >= maxLen :
      if len( arrValid ) <= 1:
        return result

      # maxLen1 = maxLen - 1
      # maxLen2 = maxLen

      # for iCnt in range( 0, maxLen1 ) :
      for iCnt in arrValid :

        # if iCnt in arrSkip:
        #   continue

        if iCnt in arrDel:
          continue

        elem = symExpr.elements[ iCnt ]

        subSet = { x for x in arrValid if x > iCnt and x not in arrDel }
        for iCnt2 in subSet :
        # for iCnt2 in range( iCnt + 1, maxLen2 ) :
        # for iCnt2 in filter( lambda x:x > iCnt, arrValid ):
        # for iCnt2 in arrValid:

          # if iCnt2 in arrSkip:
          # if iCnt2 not in arrValid:
          # if iCnt2 <= iCnt:
          #   continue

          # if iCnt2 in arrDel:
          #   continue

          elem2 = symExpr.elements[ iCnt2 ]

          if elem2.isEqual( elem, True, False ) != True:
            continue

          # 2 same function add powers
          iPowerCounter1     = elem.powerCounter  * elem.powerSign
          iPowerCounter2     = elem2.powerCounter * elem2.powerSign

          iPowerDenominator1 = elem.powerDenominator
          iPowerDenominator2 = elem2.powerDenominator

          # 2/3 + 3/5 = 2 * 5 / 3 * 5 + 3 * 3 / 5 * 3
          iPowerCounter     = iPowerCounter1 * iPowerDenominator2 + iPowerCounter2 * iPowerDenominator1
          iPowerDenominator = iPowerDenominator1 * iPowerDenominator2

          # lFound = True
          result = True

          elem.powerSign        = 1
          elem.powerCounter     = iPowerCounter
          elem.powerDenominator = iPowerDenominator

          arrDel.add( iCnt2 )
          elem = symExpr.elements[ iCnt ]

      # del elements
      for iCnt in sorted( arrDel, reverse=True):
        del symExpr.elements[ iCnt ]

      return result

    #
    # Main part multplyElements
    # .........................

    # return
    # check for symType but every routine must check it to because the simType can be changed
    if symExpr.symType != '*':
      return result
    if symExpr.numElements() <= 1:
      return result

    # debug = False
    # debug = True

    # multiply SymNumbers
    answer  = _multiplyNumbers()
    # if debug == True and answer == True:
    #   print( f"_multiplyNumbers: {str(symExpr)}")
    result |= answer

    # get all sub expressons with power op 1
    answer  = _multiplyElemGetSubPowerOne()
    # if debug == True and answer == True:
    #   print( f"_multiplyElemGetSubPowerOne: {str(symExpr)}")
    result |= answer

    # multiply SymVariable with sympexression of type +
    answer  = _multiplyElemUnitExpress()
    # if debug == True and answer == True:
    #   print( f"_multiplyElemGetSubPowerOne: {str(symExpr)}")
    result |= answer

    # multiply 2 symexpressions (type plus)
    answer  = _multiplyElemExpressExpress()
    # if debug == True and answer == True:
    #   print( f"_multiplyElemExpressExpress: {str(symExpr)}")
    result |= answer

    # multiple all SymVariable
    answer  = _multiplyElemVarVar()
    # if debug == True and answer == True:
    #   print( f"_multiplyElemVarVar: {str(symExpr)}")
    result |= answer

    # multiply number with plus expression
    answer  = _multiplyNumberExpress()
    # if debug == True and answer == True:
    #   print( f"_multiplyNumberExpress: {str(symExpr)}")
    result |= answer

    # multiply radicals with onylroots
    answer  = _multplyPlusMultiplyOnlyRoots()
    # if debug == True and answer == True:
    #   print( f"_multplyPlusMultiplyOnlyRoots: {str(symExpr)}")
    result |= answer

    # multiply radicals with onlyroots with same power
    answer  = _multplyRadicalsSamePowerOnlyRoots()
    # if debug == True and answer == True:
    #   print( f"_multplyRadicalsSamePowerOnlyRoots: {str(symExpr)}")
    result |= answer

    # multiply plus with multiply
    answer  = _multplyPlusExpressMultiply()
    # if debug == True and answer == True:
    #   print( f"_multplyPlusExpressMultiply: {str(symExpr)}")
    result |= answer

    # multiply same function = power + 1
    answer  = _multiplyFunctionFunction()
    # if debug == True and answer == True:
    #   print( f"_multiplyFunctionFunction: {str(symExpr)}")
    result |= answer

    return result

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None:
  """
  Unit test
  """

  def _Check( testClass :OptimizeMultiply
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


  # multiply SymNumbers
  symTest:symexpress3.TypVarSym3Object = symexpress3.SymFormulaParser( '2 * 3' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = typing.cast( symexpress3.SymExpress, symTest )
  symTest = symTest.elements[ 0 ]
  symOrg  = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "6" )


  # get all sub expressie with power op 1
  symTest = symexpress3.SymFormulaParser( '2 * 3 * (( 2 * 5 ))' )
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]

  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "6 * 2 * 5" )


  # multiply SymVariable with sympexression of type +
  symTest = symexpress3.SymFormulaParser( 'a * ( 2 + 3)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "(a * 2 + a * 3)" )


  # multiply 2 symexpressions (type plus)
  symTest = symexpress3.SymFormulaParser( '( a + b ) * ( c + 3)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "(a * c + a * 3 + b * c + b * 3)" )


  # multiple all SymVariable
  symTest = symexpress3.SymFormulaParser( 'a * a^2' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "a^3" )


  # multiply 2 symexpressions (type plus)
  symTest = symexpress3.SymFormulaParser( '( a + b ) * ( c + 3)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "(a * c + a * 3 + b * c + b * 3)" )


  # multiply number with plus expression
  symTest = symexpress3.SymFormulaParser( '3 * ( a + 4)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "3 * a + 3 * 4" )


  # multiply radicals with onylroots
  symTest = symexpress3.SymFormulaParser( '3^^(1/2) * 3^^(1/3)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "3^^(5/6)" )


  # multiply radicals with onlyroots with same power
  symTest = symexpress3.SymFormulaParser( '3^^(1/3) * 5^^(1/3)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "(5 * 3)^^(1/3)" )


  # multiply plus with multiply
  symTest = symexpress3.SymFormulaParser( '3 * a * ( c + d ) * e' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "3 * e * a * c + 3 * e * a * d" )


  # multiply same function = power + 1
  symTest = symexpress3.SymFormulaParser( 'cos(x) * cos(x)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "cos( x )^^2" )


  # multiply infinity
  symTest = symexpress3.SymFormulaParser( 'infinity * infinity / infinity * infinity^^(-1) * infinity' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "infinity^^3 * infinity^^-2" )


if __name__ == '__main__':
  Test( True )
