#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Gamma function for Sym Express 3

    Copyright (C) 2025 Gien van den Enden - swvandenenden@gmail.com

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


    https://en.wikipedia.org/wiki/Gamma_function

    see also optSymFunctionGammaToIntegral.py

"""

import mpmath

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase
from symexpress3         import symtools


class SymFuncGamma( symFuncBase.SymFuncBase ):
  """
  Gamma function
  """
  def __init__( self ):
    super().__init__()
    self._name        = "gamma"
    self._desc        = "Gamma function"
    self._minparams   = 1    # minimum number of parameters
    self._maxparams   = 1    # maximum number of parameters
    self._syntax      = "gamma(<n>)"
    self._synExplain  = "gamma(<n>)"

  def mathMl( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return [], None

    output = ""

    output += '<mi>&Gamma;</mi>'

    # output += "<mfenced>"

    output += elem.mathMlParameters()

    # output += "</mfenced>"

    return [], output


  def functionToValue( self, elem ):

    def _toFactorial( elem1 ):
      """
      Convert gamma to factorial
      """
      if not isinstance( elem1, symexpress3.SymNumber ) :
        return None

      if elem1.factDenominator != 1:
        return None

      if elem1.factSign != 1:
        return None

      if elem1.factCounter <= 0:
        return None

      elemNew = symexpress3.SymFunction( "factorial" )
      elemPlus = symexpress3.SymExpress( '+' )
      elemPlus.add( elem1 )
      elemPlus.add( symexpress3.SymNumber( -1, 1, 1 ) )
      elemNew.add( elemPlus )

      elemNew.powerSign        = elem.powerSign
      elemNew.powerCounter     = elem.powerCounter
      elemNew.powerDenominator = elem.powerDenominator

      return elemNew

    def _smallestGamma( elem1 ):
      """
      Convert gamma to the smallest from ( x * gammy(y) )
      """
      if not isinstance( elem1, symexpress3.SymNumber ) :
        return None

      if elem1.power != 1:
        return None

      if elem1.factSign != 1:
        return None


      # special case gamm( 1/2 ) = sqrt(pi)
      if elem1.factDenominator == 2 and elem1.factCounter == 1:
        elemNew = symexpress3.SymVariable( 'pi', 1, 1, 2, 1)

        elemRet = symexpress3.SymExpress( '*')
        elemRet.add( elemNew )
        elemRet.powerSign        = elem.powerSign
        elemRet.powerCounter     = elem.powerCounter
        elemRet.powerDenominator = elem.powerDenominator

        return elemRet


      if elem1.factDenominator == 1:
        return None

      if elem1.factCounter <= elem1.factDenominator:
        return None

      # build: product( n, 1, end, number - n * end) * gamma( module )

      endNumber = elem1.factCounter // elem1.factDenominator
      elemEnd   = symexpress3.SymNumber( 1, endNumber, 1, 1, 1, 1, 1)

      # variable name
      varName = symtools.VariableGenerateGet()
      elemVar = symexpress3.SymVariable( varName )

      # -1 * variable
      elemPlusVar = symexpress3.SymExpress( '*' )
      elemPlusVar.add( symexpress3.SymNumber( -1, 1, 1 ) )
      elemPlusVar.add( elemVar )

      # number + -1 * variable
      elemPlus = symexpress3.SymExpress( '+' )
      elemPlus.add( elem1 )
      elemPlus.add( elemPlusVar )

      # product function
      elemNew = symexpress3.SymFunction( "product" )
      elemNew.add( elemVar )
      elemNew.add( symexpress3.SymNumber( 1, 1, 1, 1, 1, 1, 1 ) )
      elemNew.add( elemEnd )
      elemNew.add( elemPlus )

      # new gamma function with only the modulo as parameter
      elemGamma = elem1.copy()
      elemGamma.factCounter = elemGamma.factCounter % elemGamma.factDenominator
      elemGamFunc = symexpress3.SymFunction( 'gamma')
      elemGamFunc.add( elemGamma )

      # product() * gamma()
      elemRet = symexpress3.SymExpress( '*')
      elemRet.add( elemNew   )
      elemRet.add( elemGamFunc )

      elemRet.powerSign        = elem.powerSign
      elemRet.powerCounter     = elem.powerCounter
      elemRet.powerDenominator = elem.powerDenominator

      return elemRet


    def _convNegative( elem1 ):
      """
      Convert negative gamma to positive gamma for non integer values
      """
      try:
        val = elem1.getValue()
      except: # pylint: disable=bare-except
        return None

      if isinstance( val, (float, mpmath.mpf )):
        if val >= 0:
          return None

        # integer values not allowed
        if mpmath.floor( val ) == mpmath.ceil( val ):
          return None

      elif isinstance( val, (complex, mpmath.mpc)):
        if val.real >= 0:
          return None

        # integer values not allowed
        if mpmath.floor( val.real ) == mpmath.ceil( val.real ):
          return None

      else:
        return None

      varElem = str( elem1 )
      cElem = f"(1/gamma( ({varElem}) * (-1) + 1)) * ( pi / sin( pi * (  ({varElem}) * (-1) + 1 ) )"

      elemNew = symexpress3.SymFormulaParser( cElem )

      elemNew.powerSign        = elem.powerSign
      elemNew.powerCounter     = elem.powerCounter
      elemNew.powerDenominator = elem.powerDenominator

      return elemNew


    if self._checkCorrectFunction( elem ) != True:
      return None

    if elem.numElements() != 1:
      return None

    elem1 = elem.elements[0]

    elemNew = _toFactorial( elem1 )
    if elemNew != None:
      return elemNew

    elemNew = _convNegative( elem1 )
    if elemNew != None:
      return elemNew

    elemNew = _smallestGamma( elem1 )
    if elemNew != None:
      return elemNew

    return elemNew


  def _getValueSingle( self, dValue, dValue2 = None ):
    return mpmath.gamma( dValue  )

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check(  testClass, symTest, value, dValue, valueCalc, dValueCalc ):
    if dValue != None:
      dValue     = round( float(dValue)    , 10 )

    if dValueCalc != None:
      dValueCalc = round( float(dValueCalc), 10 )

    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ).strip() != valueCalc or dValue != dValueCalc:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value} <> {valueCalc}, dValue:{dValue} <> {dValueCalc}' )

  symtools.VariableGenerateReset()

  symTest = symexpress3.SymFormulaParser( 'gamma( 7 )' )
  symTest.optimize()
  testClass = SymFuncGamma()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "factorial( 7 + (-1) )", 720 )


  symtools.VariableGenerateReset()

  symTest = symexpress3.SymFormulaParser( 'gamma( -1/2 )' )
  symTest.optimize()
  testClass = SymFuncGamma()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "1 *  gamma( (-1) * 1 * 2^^-1 * (-1) + 1 )^^-1 * pi *  sin( pi * ((-1) * 1 * 2^^-1 * (-1) + 1) )^^-1", -3.5449077018  )


  symtools.VariableGenerateReset()

  symTest = symexpress3.SymFormulaParser( 'gamma( 13/4 )' )
  symTest.optimizeNormal()
  testClass = SymFuncGamma()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "product( n1,1,3,(13/4) + (-1) * n1 ) *  gamma( (1/4) )", 2.54925696671852928 )


  symTest = symexpress3.SymFormulaParser( 'gamma( 1/2 )' )
  symTest.optimizeNormal()
  testClass = SymFuncGamma()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "pi^^(1/2)", 1.77245385090551602 )


if __name__ == '__main__':
  Test( True )
