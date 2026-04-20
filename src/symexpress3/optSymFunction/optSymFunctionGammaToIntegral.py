#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Cos to sum for Sym Express 3

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

    https://en.wikipedia.org/wiki/Gamma_function

"""

import mpmath

from symexpress3 import symexpress3
from symexpress3 import optFunctionBase
from symexpress3 import symtools

class OptSymFunctionGammaToIntegral( optFunctionBase.OptFunctionBase ):
  """
  Convert cos to e
  """
  def __init__( self ):
    super().__init__()
    self._name         = "gammaToIntegral"
    self._desc         = "Convert gamma to integral if the real part is positive"
    self._funcName     = "gamma"                  # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 1                        # maximum number of parameters


  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    try:
      val = elem.getValue()
    except: # pylint: disable=bare-except
      return None

    if isinstance( val, (float, mpmath.mpf )):
      if val <= 0:
        return None
    elif isinstance( val, (complex, mpmath.mpc)):
      if val.real <= 0:
        return None
    else:
      return None

    varName = symtools.VariableGenerateGet()
    varElem = str( elem.elements[ 0 ] )
    cElem = f"integral(exp( ({varElem} - 1),  {varName}) * exp({varName} * -1), {varName}, 0,infinity )"

    elemNew = symexpress3.SymFormulaParser( cElem )

    elemNew.powerSign        = elem.powerSign
    elemNew.powerCounter     = elem.powerCounter
    elemNew.powerDenominator = elem.powerDenominator

    return elemNew


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symtools.VariableGenerateReset()

  symTest = symexpress3.SymFormulaParser( "gamma(1/3)^^(-1/2)" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  # print( "symTest: " + str( symTest ))

  testClass = OptSymFunctionGammaToIntegral()
  symNew    = testClass.optimize( symTest, "gammaToIntegral" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "( integral(  exp( (1 * 3^^-1 + (-1) * 1),n1 ) *  exp( n1 * (-1) ),n1,0,infinity ))^^(-1/2)":

    print( str( symNew ).strip() )
    print( "( integral(  exp( (1 * 3^^-1 + (-1) * 1),n1 ) *  exp( n1 * (-1) ),n1,0,infinity ))^^(-1/2)" )

    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymFunction optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )

if __name__ == '__main__':
  Test( True )
