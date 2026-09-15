#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
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


    https://en.wikipedia.org/wiki/Sine_and_cosine
    https://en.wikipedia.org/wiki/Trigonometric_functions
    https://en.wikipedia.org/wiki/Inverse_trigonometric_functions

"""

import typing
import math

from symexpress3         import symexpress3
from symexpress3.symfunc import symTrigonometricData
from symexpress3.symfunc import symFuncBase
from symexpress3         import primefactor


class SymFuncTrigonoBase( symFuncBase.SymFuncBase ):
  """
  Base class for trigonometry functions
  """
  __slots__ = ()

  # sin/cos/tan are all in radius, between 0 and 2 pi
  def _optimizeSinCosTan( self, elemFunc:symexpress3.SymFunction ) -> None|symexpress3.TypVarSym3Object :
    elem = elemFunc.elements[ 0 ]
    if not isinstance( elem, symexpress3.SymExpress ):
      return None

    if elem.numElements() != 2:
      return None

    if elem.symType != '*':
      return None

    elemNum = None
    elemVar = None

    result:None|symexpress3.TypVarSym3Object = elemFunc.copy()

    result = typing.cast( symexpress3.SymExpress, result )
    elem   = result.elements[ 0 ]
    elem   = typing.cast( symexpress3.SymExpress, elem )

    if isinstance( elem.elements[0], symexpress3.SymNumber ):
      elemNum = elem.elements[0]
    elif isinstance( elem.elements[1], symexpress3.SymNumber ):
      elemNum = elem.elements[1]
    if elemNum == None:
      return None

    if isinstance( elem.elements[0], symexpress3.SymVariable):
      elemVar = elem.elements[0]
    elif isinstance( elem.elements[1], symexpress3.SymVariable ):
      elemVar = elem.elements[1]
    if elemVar == None:
      return None

    if elemVar.name != 'pi':
      return None
    if elemVar.power != 1:
      return None

    if elemNum.power != 1:
      return None

    if elemNum.factor < 0:
      imore = elemNum.factDenominator * 2
      icurr = elemNum.factCounter * elemNum.factSign
      while icurr < 0:
        icurr += imore
      elemNum.factSign    = 1
      elemNum.factCounter = icurr
    elif elemNum.factor > 2:
      imore = elemNum.factDenominator * 2
      icurr = elemNum.factCounter * elemNum.factSign
      while icurr >  2 * elemNum.factDenominator:
        icurr -= imore
      elemNum.factSign    = 1
      elemNum.factCounter = icurr
    else:
      result = None

    return result

  # convert sin() and cos()
  def _convertFuncSinCosTan( self, elem:symexpress3.SymFunction ) -> None|symexpress3.TypVarSym3Object :

    # https://www.rapidtables.com/math/trigonometry/arctan.html

    # print( "_convertFuncSinCosTan: {}".format( str( elem )))

    elem2 = elem.elements[ 0 ]
    elemNum = None
    elemVar = None
    if isinstance ( elem2, symexpress3.SymNumber ):
      if elem2.factCounter == 0:
        elemNum = elem2
      else:
        return None

    if isinstance ( elem2, symexpress3.SymVariable ):
      if elem2.name != 'pi':
        return None
      if elem2.power != 1:
        return None
      # just one (1)
      elemNum = symexpress3.SymNumber()

    if elemNum == None:
      if not isinstance( elem2, symexpress3.SymExpress ):
        return None
      if elem2.symType != '*':
        return None
      if elem2.numElements() != 2:
        return None

      if isinstance( elem2.elements[ 0 ], symexpress3.SymNumber ):
        elemNum = elem2.elements[ 0 ]
      elif isinstance( elem2.elements[ 1 ], symexpress3.SymNumber ):
        elemNum = elem2.elements[ 1 ]
      if elemNum == None:
        return None

      if isinstance( elem2.elements[ 0 ], symexpress3.SymVariable ):
        elemVar = elem2.elements[ 0 ]
      elif isinstance( elem2.elements[ 1 ], symexpress3.SymVariable ):
        elemVar = elem2.elements[ 1 ]
      if elemVar == None:
        return None

      if elemVar.power != 1:
        return None
      if elemVar.name != 'pi':
        return None

    # check for optimize values
    if ( elemNum.power != 1 or elemNum.factor < 0 or elemNum.factor > 2 ):
      return None

    iSign        = elemNum.factSign
    iCounter     = elemNum.factCounter
    iDenominator = elemNum.factDenominator

    funcname = elem.name

    # print( "search trio: {}".format( str( elem )))
    # if (iDenominator == 20):
    #   print( "search trio: {}".format( str( elem )))

    # search direct in table
    elemnew = None
    for tri in symTrigonometricData.trigonometricdata:
      if tri[ 0 ] != funcname:
        continue
      if (  tri[ 1 ] != iSign
         or tri[ 2 ] != iCounter
         or tri[ 3 ] != iDenominator
         ):
        continue

      elemnew = symexpress3.SymFormulaParser( tri[ 4 ] )
      # this radicals can only have one (positive) solution (in the trigonometricdata all the radicals are onlyone)

      # print( "elemnew: " + str(elemnew))

      elemnew.powerSign        = elem.powerSign
      elemnew.powerCounter     = elem.powerCounter
      elemnew.powerDenominator = elem.powerDenominator

      # print( "found trip: {}".format( str(elemnew) ))

      return elemnew

    # converse the sin/cos/tan between 0 and pi/4
    # sin( x ) = cos(  pi/2 - x)
    if elem.name == 'cos':
      funcname      = 'sin'
      iCounter2     = 1
      iDenominator2 = 2

      iDenominator  *= iDenominator2
      iCounter      *= iDenominator2
      iDenominator2 *= elemNum.factDenominator
      iCounter2     *= elemNum.factDenominator

      # between 0 and 2
      iCounter = iCounter2 - iCounter
      while iCounter < 0:
        iCounter += iDenominator * 2

      # lowest form
      iGcd = math.gcd( iCounter, iDenominator )
      if iGcd != 1:
        iCounter     //= iGcd
        iDenominator //= iGcd

      # print( "cos counter:{}, denominator: {}, orginal: {}".format( iCounter, iDenominator , str( elem2)))

    cMultiple = ''
    dFactor   = iCounter / iDenominator


    iCountOrg = iCounter
    iDenomOrg = iDenominator

    # print( f"funcname: {funcname}, dFactor: {dFactor}" )

    # pylint: disable=chained-comparison
    if funcname == 'sin':
      if ( dFactor >= 0 and dFactor <= 0.5 ):
        # iCounter     = iCounter
        # iDenominator = iDenominator
        pass
      elif ( dFactor >= 0.5 and dFactor <= 1 ):
        iCounter     = 1 * iDenominator - iCounter
        # iDenominator = iDenominator
      elif ( dFactor >= 1 and dFactor <= 1.5 ):
        # iCounter     = ( 1 * iDenominator - iCounter ) + 1 * iDenominator
        iCounter     = iCounter - iDenominator
        # iDenominator = iDenominator
        cMultiple    = '-1 * '
      elif ( dFactor >= 1.5 and dFactor <= 2 ):
        iCounter     = 2 * iDenominator - iCounter
        # iDenominator = iDenominator
        cMultiple    = '-1 * '
    elif funcname == 'tan':
      if ( dFactor >= 0 and dFactor <= 0.5 ):
        # iCounter     = iCounter
        # iDenominator = iDenominator
        pass
      elif ( dFactor >= 0.5 and dFactor <= 1 ):
        iCounter     = 1 * iDenominator - iCounter
        # iDenominator = iDenominator
        cMultiple    = '-1 * '
      elif ( dFactor >= 1 and dFactor <= 1.5 ):
        # iCounter     = ( 1 * iDenominator - iCounter ) + 1 * iDenominator
        iCounter     = iCounter - iDenominator
        # iDenominator = iDenominator
      elif ( dFactor >= 1.5 and dFactor <= 2 ):
        iCounter     = 2 * iDenominator - iCounter
        # iDenominator = iDenominator
        cMultiple    = '-1 * '


    # print( "cos counter:{}, denominator: {}, dFactor: {}, orginal: {}".format( iCounter, iDenominator , dFactor, str( elem2)))
    elemnew = None
    for tri in symTrigonometricData.trigonometricdata:
      if tri[ 0 ] != funcname:
        continue
      if (  tri[ 1 ] != iSign
         or tri[ 2 ] != iCounter
         or tri[ 3 ] != iDenominator
         ):
        continue

      # print( f"funcname: {funcname}, iSign: {iSign}, iCounter: {iCounter}, iDenominator:{iDenominator}, cMultiple: {cMultiple} " )
      elemnew = symexpress3.SymFormulaParser( cMultiple + "(" + tri[ 4 ] + ")" )
      # this radicals can only have one (positive) solution (in the trigonometricdata all the radicals are onlyone)

      # print( "elemnew: " + str(elemnew))

      elemnew.powerSign        = elem.powerSign
      elemnew.powerCounter     = elem.powerCounter
      elemnew.powerDenominator = elem.powerDenominator

      break
    # print( "elemnew: " + str(elemnew))

    if elemnew == None:
      # try to create the sin/cos formula
      formualSinCos = self._getSinCos( funcname, iCountOrg, iDenomOrg)
      if formualSinCos != None:
        elemnew = symexpress3.SymFormulaParser( formualSinCos )
        elemnew.powerSign        = elem.powerSign
        elemnew.powerCounter     = elem.powerCounter
        elemnew.powerDenominator = elem.powerDenominator

    return elemnew


  #
  # get the sin/cos from the given counter/denominator
  # if not exist try to create one (with only real radicals, no complex)
  #
  def _getSinCos( self, cType:str, iCounter:int, iDenominator:int ) -> None|str :

    # search trigonometricdata to the given base
    def _getBaseFormula( cTp:str, iCount:int, iDenom:int ) -> None|str :
      for tri in symTrigonometricData.trigonometricdata:
        if tri[ 0 ] != cTp:
          continue
        if tri[ 1 ] != 1:  # type
          continue
        if tri[ 2 ] != iCount:
          continue
        if tri[ 3 ] != iDenom:
          continue

        return typing.cast( str, tri[ 4 ] ) # symexpress string formula

      return None

    def _createSinCosHalf( iDenom:int ) -> None :
      # sin( x / 2 ) = sign( sin( x/2 ) ) ( (1 - cos(x) ) / 2 )^^(1/2)
      # cos( x / 2 ) = sign( cos( x/2 ) ) ( (1 + cos(x) ) / 2 )^^(1/2)

      baseNum = iDenom // 2

      # it always in  first quarter, no sign needed
      formulaSin = f"( (1 - cos( pi / {baseNum}) ) / 2 )^^(1/2)"
      formulaCos = f"( (1 + cos( pi / {baseNum}) ) / 2 )^^(1/2)"

      oFormulaSin = symexpress3.SymFormulaParser( formulaSin )
      oFormulaCos = symexpress3.SymFormulaParser( formulaCos )

      oFormulaSin.optimizeNormal( extra=['nodebug'] )
      oFormulaCos.optimizeNormal( extra=['nodebug'] )

      triRec = [
          "sin"
        , 1
        , 1
        , iDenom
        , str( oFormulaSin )
        , None
      ]

      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add sin: { triRec[ 4 ]}" )

      triRec = [
          "cos"
        , 1
        , 1
        , iDenom
        , str( oFormulaCos )
        , None
      ]

      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add cos: { triRec[ 4 ]}" )

    def _createSinCosDouble( iCount:int, iDenom:int ) -> None :
      # sin( 2x ) = 2 sin(x) cos(x)
      # cos( 2x ) = 2 cos(x)^^2 - 1

      baseCount = iCount // 2

      formulaSin = f"2 sin( pi {baseCount} / {iDenom}) cos(pi {baseCount} / {iDenom})"
      formulaCos = f"2 cos(pi {baseCount} / {iDenom})^^2 - 1"

      oFormulaSin = symexpress3.SymFormulaParser( formulaSin )
      oFormulaCos = symexpress3.SymFormulaParser( formulaCos )

      oFormulaSin.optimizeNormal( extra=['nodebug'] )
      oFormulaCos.optimizeNormal( extra=['nodebug'] )

      triRec = [
          "sin"
        , 1
        , iCount
        , iDenom
        , str( oFormulaSin )
        , None
      ]
      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add sin: { triRec[ 4 ]}" )

      triRec = [
           "cos"
         , 1
         , iCount
         , iDenom
         , str( oFormulaCos )
         , None
      ]
      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add cos: { triRec[ 4 ]}" )

    def _createSinCosPlusOne( iCount:int, iDenom:int ) -> None :
      # sin( x + y ) = sin(x) cos(y) + cos(x) sin(y)
      # cos( x + y ) = cos(x) cos(y) - sin(x) sin(y)
      # sin( x - y ) = sin(x) cos(y) - cos(x) sin(y)
      # cos( x - y ) = cos(x) cos(y) - sin(x) sin(y)

      baseCount = iCount - 1
      # x = baseCount
      # y = 1
      formulaSin = f"sin( pi {baseCount} / {iDenom} ) cos( pi / {iDenom} ) + cos( pi {baseCount} / {iDenom} ) sin( pi / {iDenom} )"
      formulaCos = f"cos(pi {baseCount} / {iDenom}  ) cos( pi / {iDenom} ) - sin( pi {baseCount} / {iDenom} ) sin( pi / {iDenom} )"

      # print( f"formulaSin: {formulaSin}" )
      # print( f"formulaCos: {formulaSin}" )

      oFormulaSin = symexpress3.SymFormulaParser( formulaSin )
      oFormulaCos = symexpress3.SymFormulaParser( formulaCos )

      oFormulaSin.optimizeNormal( extra=['nodebug'] )
      oFormulaCos.optimizeNormal( extra=['nodebug'] )

      triRec = [
           "sin"
         , 1
         , iCount
         , iDenom
         , str( oFormulaSin )
         , None
      ]
      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add sin: { triRec[ 4 ]}" )

      triRec = [
          "cos"
        , 1
        , iCount
        , iDenom
        , str( oFormulaCos )
        , None
      ]
      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add cos: { triRec[ 4 ]}" )


    # only positive hooks
    if iCounter <= 0:
      return None

    if iDenominator <= 0:
      return None

    # 2 pi is max
    if iCounter >= iDenominator * 2 :
      return None

    # only sin and cos supported
    if not cType in ("sin", "cos" ):
      return None

    dictFactors = primefactor.FactorizationDict( iDenominator )

    # print( dictFactors );

    # only support 2, 3 and 5
    # other numbers will give complex radicals
    baseNumber = 1
    for key, value in dictFactors.items():
      if key == 2:
        baseNumber *= key
      elif key == 3:
        if value != 1:
          return None
        baseNumber *= key
      elif key == 5 :
        if value != 1:
          return None
        baseNumber *= key
      else:
        return None

    if baseNumber % 2 == 0:
      baseNumber //= 2

    if baseNumber == 1:
      return None

    # print( f"BaseNumber: {baseNumber}" )

    baseFormula = _getBaseFormula( cType, 1, baseNumber )
    if baseFormula == None:
      return None


    # get all the half numbers
    while baseNumber < iDenominator:
      baseNumber *= 2

      baseForm2 = _getBaseFormula( cType, 1, baseNumber )
      if baseForm2 == None:
        # print( f"Create new {baseNumber}" )
        # create new base formula
        _createSinCosHalf( baseNumber )

    # get the counter of the base
    baseFormula = _getBaseFormula( cType, iCounter, baseNumber )
    iCount = 1
    while baseFormula == None and iCount <= iCounter :
      iCount *= 2
      if iCount <= iCounter:
        # print( f"Add double {iCount} / {baseNumber}" )
        _createSinCosDouble( iCount, baseNumber )
      else:
        baseFormula = None
        break
      baseFormula = _getBaseFormula( cType, iCounter, baseNumber )

    if baseFormula == None:
      iCount //= 2
      while baseFormula == None and iCount <= iCounter:
        # add one
        iCount += 1
        # print( f"Add one {iCount} / {baseNumber}" )
        _createSinCosPlusOne( iCount, baseNumber )
        baseFormula = _getBaseFormula( cType, iCounter, baseNumber )

    # print( baseFormula );
    return baseFormula


  def _convertSinCosAtan( self, elem:symexpress3.SymFunction ) -> None|symexpress3.TypVarSym3Object :
    #
    # convert sin/cos/tan( asin/acos/atan() )
    # convert sin/cos(x/2))
    #
    # https://en.wikipedia.org/wiki/Inverse_trigonometric_functions
    #
    if elem.numElements() != 1:
      return None

    if isinstance( elem.elements[ 0 ], symexpress3.SymFunction ):
      elemfunc = elem.elements[ 0 ]

      if elemfunc.name == 'atan':

        # sin( arctan(x)) = x / sqrt( 1+x^2 )
        # cos( arctan(x)) = 1 / sqrt( 1+x^2)
        # tan( arctan(x)) = x

        if elem.name == 'tan':
          strResult = str( elemfunc.elements[ 0 ] )
        else:
          strFunc   = '(' + str( elemfunc.elements[ 0 ] ) + ')'
          strSqrt   = '( 1 + ' + strFunc + '^^2)^^(1/2)'
          strResult = ''
          if elem.name == 'sin':
            strResult = strFunc + '/' + strSqrt
          elif elem.name == 'cos':
            # cos
            strResult = '1 /' + strSqrt
          else:
            return None # should not occur

      elif elemfunc.name == 'asin':

        # sin( asin(x)) = x
        # cos( asin(x)) = sqrt( 1 - x^2)
        # tan( asin(x)) = x / sqrt( 1 - x^2 )

        if elem.name == 'sin':
          strResult = str( elemfunc.elements[ 0 ] )
        else:
          strFunc   = '(' + str( elemfunc.elements[ 0 ] ) + ')'
          strSqrt   = '( 1 - ' + strFunc + '^^2)^^(1/2)'
          strResult = ''
          if elem.name == 'tan':
            strResult = strFunc + '/' + strSqrt
          elif elem.name == 'cos':
            # cos
            strResult = strSqrt
          else:
            return None # should not occur

      elif elemfunc.name == 'acos':

        # sin( acos(x)) = sqrt( 1 - x^2 )
        # cos( acos(x)) = x
        # tan( acos(x)) = sqrt( 1 - x^2 ) / x

        if elem.name == 'cos':
          strResult = str( elemfunc.elements[ 0 ] )
        else:
          strFunc   = '(' + str( elemfunc.elements[ 0 ] ) + ')'
          strSqrt   = '( 1 - ' + strFunc + '^^2)^^(1/2)'
          strResult = ''
          if elem.name == 'tan':
            strResult = strSqrt + '/' + strFunc
          elif elem.name == 'sin':
            # cos
            strResult = strSqrt
          else:
            return None # should not occur
      else:
        return None # nothing to do

      exprResult = symexpress3.SymFormulaParser( '(' + strResult + ')' )
      exprResult.powerSign        = elem.powerSign
      exprResult.powerCounter     = elem.powerCounter
      exprResult.powerDenominator = elem.powerDenominator
      exprResult.optimizeNormal( extra=['nodebug'] )

      # print( 'exprResult: {}'.format( str( exprResult ) ))

      return exprResult

    if isinstance( elem.elements[ 0 ], symexpress3.SymExpress ):
      #
      # cos(x/2) = sqrt( (1 + cos(x)) / 2 )
      # sin(x/2) = sqrt( (1 - cos(x)) / 2 )
      # replace 2 to a power of 2 and make x atan(y) then that's it
      #
      elemexpr = elem.elements[ 0 ]
      # elemexpr = typing.cast( symexpress3.SymExpress, elemexpr )

      if elemexpr.symType == '*' and elemexpr.numElements() == 2 and elemexpr.power == 1:
        if isinstance( elemexpr.elements[ 0 ], symexpress3.SymFunction ):
          elemFunc:symexpress3.TypVarSym3Object = elemexpr.elements[ 0 ]
          elemNum                               = elemexpr.elements[ 1 ]
        else:
          elemFunc = elemexpr.elements[ 1 ]
          elemNum  = elemexpr.elements[ 0 ]

        if (   isinstance( elemFunc, symexpress3.SymFunction )
            and elemFunc.name       == 'atan'
            and elemFunc.power      == 1
            and isinstance( elemNum, symexpress3.SymNumber )
            and elemNum.power       == 1
            and elemNum.factSign    == 1
            and elemNum.factCounter == 1
           ):

          # ok, found atan(x)/y
          dictFactors = primefactor.FactorizationDict( elemNum.factDenominator )

          if len( dictFactors ) == 1 and 2 in dictFactors:

            # ok elemNumm is a power of 2 (2^x)
            factor = elemNum.factDenominator // 2

            if elem.name == 'cos':
              elemStr = f"( (1 + cos( {str(elemFunc)} / {factor} )) / 2 )^^(1/2)"
            elif elem.name == 'sin':
              elemStr = f"( (1 - cos( {str(elemFunc)}/ {factor})) / 2 )^^(1/2)"
            else:
              elemStr = ''

            if elemStr != '':
              exprResult = symexpress3.SymFormulaParser( elemStr )
              exprResult.powerSign        = elem.powerSign
              exprResult.powerCounter     = elem.powerCounter
              exprResult.powerDenominator = elem.powerDenominator
              exprResult.optimizeNormal( extra=['nodebug'] )

              return exprResult

    return None

  def _convertSinCosTanAtanSign( self, elem:symexpress3.SymFunction ) -> None|symexpress3.TypVarSym3Object :
    #  sin( -x ) = - sin(  x )
    #  cos( -x ) = + cos(  x )
    #  tan( -x ) = - tan(  x )
    # atan( -x ) = - atan( x )
    # asin( -x ) = - asin( x )
    # acos( -x ) = pi - acos( x )

    if elem.numElements() != 1:
      return None

    elem1 = elem.elements[ 0 ]
    if isinstance( elem1, symexpress3.SymNumber ):
      if (elem1.power != 1 or elem1.factSign == 1 ):
        return None

      elemExpress    = elem.copy()
      elem1          = elemExpress.elements[ 0 ]
      elem1          = typing.cast( symexpress3.SymNumber, elem1 )
      elem1.factSign = 1

      if elemExpress.name == "cos":
        elemResult:symexpress3.TypVarSym3Object = elemExpress

      elif elemExpress.name == "acos":
        elemResult = symexpress3.SymExpress( '+' )
        elemResult.add( symexpress3.SymVariable( 'pi' ))

        elemExtra = symexpress3.SymExpress('*')
        elemExtra.add( symexpress3.SymNumber( -1, 1, 1 ) )
        elemExtra.add( elemExpress )

        elemResult.add( elemExtra )
      else:
        elemResult = symexpress3.SymExpress('*')
        elemResult.add( symexpress3.SymNumber( -1, 1, 1, 1, 1, 1, 1) )
        elemResult.add( elemExpress )

      return elemResult

    if not isinstance( elem1, symexpress3.SymExpress ):
      return None

    if elem1.symType != '*':
      return None

    # search for a negative number
    foundNo = -1
    for iCnt, elemTest in enumerate( elem1.elements ):
      if not isinstance( elemTest, symexpress3.SymNumber ):
        continue
      if (elemTest.power != 1) or (elemTest.factSign == 1):
        continue
      # ok, found one
      foundNo = iCnt
      break

    if foundNo == -1:
      return None

    elemExpress    = elem.copy()
    elem1          = elemExpress.elements[ 0 ].elements[ foundNo ] # type:ignore
    elem1          = typing.cast( symexpress3.SymNumber, elem1 )
    elem1.factSign = 1

    if elemExpress.name == "cos":
      elemResult = elemExpress

    elif elemExpress.name == "acos":
      elemResult = symexpress3.SymExpress( '+' )
      elemResult.add( symexpress3.SymVariable( 'pi' ))

      elemExtra = symexpress3.SymExpress('*')
      elemExtra.add( symexpress3.SymNumber( -1, 1, 1 ) )
      elemExtra.add( elemExpress )

      elemResult.add( elemExtra )
    else:
      elemResult = symexpress3.SymExpress('*')
      elemResult.add( symexpress3.SymNumber( -1, 1, 1, 1, 1, 1, 1) )
      elemResult.add( elemExpress )

    return elemResult

  def _conversTableToArc( self, elem:symexpress3.SymFunction ) -> None|symexpress3.TypVarSym3Object :
    funcname = None
    if elem.name == 'atan':
      funcname = 'tan'
    elif elem.name == 'asin':
      funcname = "sin"
    elif elem.name == "acos":
      funcname = "cos"

    if funcname == None:
      return None

    exp = elem.elements[ 0 ]

    # print( "funcname: {}, exp: {}, type: {}".format( funcname, str( exp ), type( exp ) ))

    for tri in symTrigonometricData.trigonometricdata:

      if tri[ 0 ] != funcname:
        continue

      # convert string to expression
      if tri[ 5 ] == None:
        tri[ 5 ] = symexpress3.SymFormulaParser( tri[ 4 ] )
        tri[ 5 ].optimizeNormal( extra=['nodebug'] )
        if tri[ 5 ].numElements() == 1:
          tri[ 5 ] = tri[ 5 ].elements[ 0 ]

      # print( "found {}, expr: {}, type: {}".format( tri[ 0 ], str( tri[ 5 ] ), type( tri[5] ) ) )

      if not exp.isEqual( tri[ 5 ] ):
        continue

      # found one
      angle = ''
      if tri [ 1 ] == -1:
        angle += '-1 '

      angle += str( tri[ 2 ] ) + ' / ' + str( tri[ 3 ] ) + ' * pi '

      newelem = symexpress3.SymFormulaParser( angle )
      newelem.powerSign        = elem.powerSign
      newelem.powerCounter     = elem.powerCounter
      newelem.powerDenominator = elem.powerDenominator

      return newelem

    return None
