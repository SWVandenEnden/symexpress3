#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Write out powers for Sym Express 3

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

import mpmath

from symexpress3          import symexpress3
from symexpress3.optimize import optimizeBase

class OptimizePower( optimizeBase.OptimizeBase ):
  """
  Write out all the powers greater then one so that they become one.
  \n (x+1)^2 becomes (x+1)(x+1)
  """
  def __init__( self ):
    super().__init__()
    self._name         = "power"
    self._symtype      = "all"
    self._desc         = "Write out all the powers greater then one"


  def optimize( self, symExpr, action ):
    result = False

    if self.checkExpression( symExpr, action ) != True:
      # print( "Afgekeurd: " + symExpr.symType )
      return result

    # auto set onlyOneRoot
    if symExpr.powerDenominator == 1 and symExpr.onlyOneRoot != 1:
      symExpr.onlyOneRoot = 1

    if ( symExpr.powerCounter  < 2 or
         symExpr.onlyOneRoot  != 1 or
         symExpr.numElements() < 2
       ):
      return result

    if (symExpr.powerDenominator > 1 and symExpr.onlyOneRoot == 1):
      # (x+2)^^(2/3)
      # first calc the 1/3 principal root then the power
      # if number >= 0 you can do the power
      try:
        calcReal = symExpr.getValue()
      except: # pylint: disable=bare-except
        return False

      if isinstance( calcReal, list ):
        return False

      if isinstance( calcReal, (complex, mpmath.mpc) ):
        return False

      if calcReal < 0:
        return False

    # https://en.wikipedia.org/wiki/Binomial_theorem
    if symExpr.symType == '+' :

      elemX = symExpr.elements[0]
      elemY = symexpress3.SymExpress( '+' )
      for iCnt in range( 1, symExpr.numElements() ):
        elemY.elements.append( symExpr.elements[iCnt] )

      elemPlus = symexpress3.SymExpress( '+' )

      numN = symExpr.powerCounter
      for iCnt in range( 0, numN + 1 ):
        bioNum      = int( mpmath.binomial(numN,iCnt) )
        symBiominal = symexpress3.SymNumber( 1, bioNum, 1)

        elemXBio = symexpress3.SymExpress( '*')
        elemXBio.add( elemX )
        elemXBio.powerCounter = numN - iCnt

        elemYBio = symexpress3.SymExpress( '*')
        elemYBio.add( elemY )
        elemYBio.powerCounter = iCnt

        elemAdd = symexpress3.SymExpress( '*')
        elemAdd.elements.append( symBiominal )
        elemAdd.elements.append( elemXBio    )
        elemAdd.elements.append( elemYBio    )

        elemPlus.add( elemAdd )

      symExpr.elements     = elemPlus.elements
      symExpr.powerCounter = 1

    else:
      # multiply
      elemNew = symexpress3.SymExpress( '*' )
      for elem in symExpr.elements :
        elemClone = symexpress3.SymExpress( '*' )
        elemClone.powerCounter = symExpr.powerCounter
        elemClone.add( elem )
        elemNew.elements.append( elemClone )

      symExpr.symType      = '*'
      symExpr.elements     = elemNew.elements
      symExpr.powerCounter = 1

    result               = True

    return result

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check( testClass, symOrg, symTest, wanted ):
    if display == True :
      print( f"naam      : {testClass.name}" )
      print( f"orginal   : {str( symOrg  )}" )
      print( f"optimized : {str( symTest )}" )

    if str( symTest ).strip() != wanted:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}' )

  result = False
  symTest = symexpress3.SymFormulaParser( '(a + b)^^2' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  symOrg = symTest.copy()

  testClass = OptimizePower()
  result |= testClass.optimize( symTest, "power" )

  _Check( testClass, symOrg, symTest, "1 * (a)^^2 * (b)^^0 + 2 * a * b + 1 * (a)^^0 * (b)^^2" )


  symTest = symexpress3.SymFormulaParser( '(a * b)^^2' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  symOrg = symTest.copy()

  testClass = OptimizePower()
  testClass.optimize( symTest, "power" )

  _Check( testClass, symOrg, symTest, "(a)^^2 * (b)^^2" )


  symTest = symexpress3.SymFormulaParser( '(a + b)^^3' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizePower()
  result |= testClass.optimize( symTest, "power" )

  _Check( testClass, symOrg, symTest, "1 * (a)^^3 * (b)^^0 + 3 * (a)^^2 * b + 3 * a * (b)^^2 + 1 * (a)^^0 * (b)^^3" )


if __name__ == '__main__':
  Test( True )
