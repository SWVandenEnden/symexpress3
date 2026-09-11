#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Exp function voor Sym Express 3

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


    https://en.wikipedia.org/wiki/Exponential_function

"""
import typing
import mpmath # type:ignore

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase

class SymFuncExp( symFuncBase.SymFuncBase ):
  """
  Exp function, exponent, exp( x, y ) = y^x
  Default for y = e
  """
  __slots__ = ()

  def __init__( self ) -> None :
    super().__init__()
    self._name      = "exp"
    self._desc      = "Exponent, y^^x, default is e (e^^x)"
    self._minparams = 1    # minimum number of parameters
    self._maxparams = 2    # maximum number of parameters
    self._syntax    = "exp(<x> [,<y>])"
    self._synExplain= "exp(<x> [,<y>]) = y^^x, default is e (e^^x)"

  def mathMl( self, elem:None|symexpress3.TypVarSym3Object ) -> tuple[list[str], None|str]:

    if self._checkCorrectFunction( elem ) != True:
      return [], None

    elem = typing.cast( symexpress3.SymFunction, elem )

    output = ""

    output += '<msup>'

    if elem.numElements() == 2:

      isExtraClose = True
      if (     isinstance( elem.elements[ 1 ], symexpress3.SymNumber )
         and elem.elements[ 1 ].power           == 1
         and elem.elements[ 1 ].factDenominator == 1
         and elem.elements[ 1 ].factSign        == 1 ):
        isExtraClose = False

      if (     isinstance( elem.elements[ 1 ], symexpress3.SymVariable )
         and elem.elements[ 1 ].power           == 1         ):
        isExtraClose = False

      if isExtraClose == True:
        # output += "<mfenced separators=''>"
        output += "<mrow><mo>(</mo>"

      output += elem.elements[ 1 ].mathMl()

      if isExtraClose == True:
        # output += "</mfenced>"
        output += "<mo>)</mo></mrow>"
    else:
      output += '<mi>'
      output += 'e'
      output += '</mi>'

    output += elem.elements[ 0 ].mathMl()

    output += '</msup>'

    return ['()'], output


  def functionToValue( self, elem:None|symexpress3.TypVarSym3Object ) -> None|symexpress3.TypVarSym3Object :

    if self._checkCorrectFunction( elem ) != True:
      return None

    elem = typing.cast( symexpress3.SymFunction, elem )

    if elem.onlyOneRoot != 1:
      return None

    # exp(a)^^2 = exp( 2 * a )
    if elem.onlyOneRoot == 1 and (elem.powerSign != 1 or elem.powerCounter != 1 or elem.powerDenominator != 1):
      elemPower = symexpress3.SymNumber( elem.powerSign, elem.powerCounter, elem.powerDenominator )

      elemNew = elem.copy()
      elemNew.powerSign        = 1
      elemNew.powerCounter     = 1
      elemNew.powerDenominator = 1

      elemNum1 = symexpress3.SymExpress( '*' )
      elemNum1.add( elemNew.elements[0] )
      elemNum1.add( elemPower )
      elemNew.elements[ 0 ] = elemNum1

      return elemNew


    # (x^2)^y = x^( 2 * y )
    # elem1 = y
    # elem2 = x
    if elem.numElements() == 2:
      elem1 = elem.elements[ 0 ]
      elem2 = elem.elements[ 1 ]
      if elem2.onlyOneRoot == 1 and elem2.power != 1:
        elemXNew = elem2.copy()
        elemXNew.powerSign        = 1
        elemXNew.powerCounter     = 1
        elemXNew.powerDenominator = 1

        # may not if elemXNew <= 0
        # below transformation is only valid if valX > 0
        posVal = True
        try:
          valX = elemXNew.getValue()
          if valX <= 0 : #type:ignore
            posVal = False
        except: # pylint: disable=bare-except
          posVal = False

        if posVal == True:
          elemYNew = symexpress3.SymExpress( '*' )
          elemYNew.add( elem1 )
          elemXPower = symexpress3.SymNumber( elem2.powerSign, elem2.powerCounter, elem2.powerDenominator )
          elemYNew.add( elemXPower )

          elemNew = symexpress3.SymFunction( 'exp' )
          elemNew.add( elemYNew )
          elemNew.add( elemXNew )

          elemNew.powerSign        = elem.powerSign
          elemNew.powerCounter     = elem.powerCounter
          elemNew.powerDenominator = elem.powerDenominator

          return elemNew


    # exp( 3 log(2) ) = exp( 3, 2 )
    if elem.numElements() == 1:
      elem1 = elem.elements[ 0 ]
      if isinstance( elem1, symexpress3.SymFunction ):
        if elem1.name == 'log' and elem1.power == 1 :
          if elem1.numElements() == 1:
            elemNew = symexpress3.SymFunction( 'exp' )
            elemNew.add( symexpress3.SymNumber( 1,1,1 ) ) # one
            elemNew.add( elem1.elements[0] )

            elemNew.powerSign        = elem.powerSign
            elemNew.powerCounter     = elem.powerCounter
            elemNew.powerDenominator = elem.powerDenominator

            return elemNew
      elif isinstance( elem1, symexpress3.SymExpress ):
        if elem1.symType == '*' and elem1.power == 1:
          for iCnt, elem2 in enumerate( elem1.elements ):
            if isinstance( elem2, symexpress3.SymFunction ):
              if elem2.name == 'log' and elem2.power == 1  and elem2.numElements() == 1:
                elemNew = elem.copy()
                elemNew.add( elem2.elements[0])
                del elemNew.elements[ 0 ].elements[ iCnt ] # type:ignore
                return elemNew

    # exp( 3 log(5,2) ,2 ) = exp( 3, 5 )
    if elem.numElements() == 2:
      if isinstance( elem1, symexpress3.SymFunction ):
        if elem1.name == 'log' and elem1.power == 1 :
          if elem1.numElements() == 2 and elem1.elements[1].isEqual( elem.elements[1]):
            elemNew = symexpress3.SymFunction( 'exp' )
            elemNew.add( symexpress3.SymNumber( 1,1,1 ) ) # one
            elemNew.add( elem1.elements[0] )

            elemNew.powerSign        = elem.powerSign
            elemNew.powerCounter     = elem.powerCounter
            elemNew.powerDenominator = elem.powerDenominator

            return elemNew

      elif isinstance( elem1, symexpress3.SymExpress ):
        if elem1.symType == '*' and elem1.power == 1:
          for iCnt, elem2 in enumerate( elem1.elements ):
            if isinstance( elem2, symexpress3.SymFunction ):
              if (    elem2.name == 'log'
                  and elem2.power == 1
                  and elem2.numElements() == 2
                  and elem2.elements[1].isEqual( elem.elements[1] )
                 ):
                elemNew = elem.copy()
                elemNew.elements[1] = elem2.elements[0]
                del elemNew.elements[ 0 ].elements[ iCnt ] # type:ignore
                return elemNew

    #
    # x^y
    # elem1 = y
    # elem2 = x if not provided, e is used
    #
    elem1 = elem.elements[ 0 ]


    if not isinstance ( elem1, symexpress3.SymNumber ):
      return None

    if elem1.power != 1:
      return None

    if elem.numElements() < 2:
      elemBase = "e"
    else:
      # array not supported, use expandArray
      if isinstance ( elem.elements[ 1 ], symexpress3.SymArray ):
        return None
      elemBase = str( elem.elements[ 1 ] )

    # print("_convertFuncExp elem1: {}".format(elem1) )
    if str( elem1 ) == "0":
      elemStr = "1"
    else:
      elemStr = "(" + elemBase + ")^^(" + str( elem1 ) + ")"
    # print( "_convertFuncExp: {}".format( elemStr ))

    elemnew = symexpress3.SymFormulaParser( elemStr )

    elemnew.powerSign        = elem.powerSign
    elemnew.powerCounter     = elem.powerCounter
    elemnew.powerDenominator = elem.powerDenominator

    return elemnew


  def _getValueSingle( self, dValue:symexpress3.TypVarSym3Value, dValue2:None|symexpress3.TypVarSym3Value = None ) -> symexpress3.TypVarSym3Value :
    if dValue2 == None:
      dValue2 = mpmath.e

    dResult = dValue2 ** dValue
    # dResult = mpmath.root( dValue2, dValue )
    return dResult


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display:bool = False) -> None :
  """
  Unit test
  """
  def _Check( testClass :SymFuncExp
            , symTest   :symexpress3.TypVarSym3Object
            , value     :None|symexpress3.TypVarSym3Object
            , dValue    :symexpress3.TypVarSym3Value
            , valueCalc :None|str
            , dValueCalc:symexpress3.TypVarSym3Value
            ) -> None :

    if dValue != None:
      dValue = symexpress3.SymRound( dValue, 10 )

    if dValueCalc != None:
      dValueCalc = symexpress3.SymRound( dValueCalc, 10 )

    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if value == None and valueCalc == None:
      return

    if str( value ).strip() != valueCalc or (dValueCalc != None and dValue != dValueCalc) : # pylint: disable=consider-using-in
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value} <> {valueCalc}, dValue:{dValue} <> {dValueCalc}' )

  symTest = symexpress3.SymFormulaParser( 'exp( 2 ,10 )' )
  symTest.optimize()
  exp    = SymFuncExp()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = exp.getValue(        symTest.elements[ 0 ] )

  _Check( exp, symTest, value, dValue, "(10)^^2", 100 )


  symTest = symexpress3.SymFormulaParser( 'exp( 2 )' )
  symTest.optimize()
  exp    = SymFuncExp()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = exp.getValue(        symTest.elements[ 0 ] )

  _Check( exp, symTest, value, dValue, "(e)^^2", 7.3890560989 )


  symTest = symexpress3.SymFormulaParser( ' exp( 2 * n + 1,x^^3 )' )
  symTest.optimize()
  exp    = SymFuncExp()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = None

  # _Check( exp, symTest, value, dValue, "exp( (2 * n + 1) * 3,x )", None )
  _Check( exp, symTest, value, dValue, None, None )


  symTest = symexpress3.SymFormulaParser( 'exp( (1/60) * i * pi )^^5' )
  symTest.optimize()
  exp    = SymFuncExp()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = None

  _Check( exp, symTest, value, dValue, "exp( (1/60) * i * pi * 5 )", None )



  symTest = symexpress3.SymFormulaParser( 'exp( log(3))' )
  symTest.optimize()
  exp    = SymFuncExp()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = None

  _Check( exp, symTest, value, dValue, "exp( 1,3 )", None )


  symTest = symexpress3.SymFormulaParser( 'exp( 2 log(3))' )
  symTest.optimize()
  exp    = SymFuncExp()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = None

  _Check( exp, symTest, value, dValue, "exp( 2,3 )", None )


  symTest = symexpress3.SymFormulaParser( 'exp( log(5,2) ,2 )' )
  symTest.optimize()
  exp    = SymFuncExp()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = None

  _Check( exp, symTest, value, dValue, "exp( 1,5 )", None )


  symTest = symexpress3.SymFormulaParser( 'exp( 3 * log(5,2) ,2 )' )
  symTest.optimize()
  exp    = SymFuncExp()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = None

  _Check( exp, symTest, value, dValue, "exp( 3,5 )", None )


  symTest = symexpress3.SymFormulaParser( 'exp( 3 * log(5,-2) ,-2^^2 )' )
  symTest.optimize()
  exp    = SymFuncExp()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = None

  _Check( exp, symTest, value, dValue, None, None )



if __name__ == '__main__':
  Test( True )
