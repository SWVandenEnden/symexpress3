#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Hypergeometric to Product for Sym Express 3

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


    See also symFuncHypergeometric.py


    https://en.wikipedia.org/wiki/Generalized_hypergeometric_function

    https://docs.sympy.org/latest/modules/simplify/hyperexpand.html
    https://github.com/sympy/sympy/blob/master/sympy/simplify/hyperexpand.py

    https://mathoverflow.net/questions/424518/does-any-hyper-geometric-function-can-be-analytically-continuated-to-the-whole-c
    https://dlmf.nist.gov/15.2
    https://encyclopediaofmath.org/wiki/Hypergeometric_function
    https://fa.ewi.tudelft.nl/~koekoek/documents/wi4006/hyper.pdf

    analytic continuation of 2F1
    https://www.sciencedirect.com/science/article/pii/S0377042700002673



    _2F_1(a, b; c; z) = (1-z)^{-a} {}_2F_1(c-a, b; c; 1-z).

    Kummer's transformation


    https://functions.wolfram.com/PDF/Hypergeometric2F1.pdf

    ChatGP2: Written the same as Wolfram but with 2F1 in steeds of sums
    2F1(a,b;c;z) = (Γ(b)Γ(c−a)) / (Γ(c)Γ(b−a)) * (−z)^−a * 2F1(a,a−c+1;a−b+1;1/z) + (Γ(a)Γ(c−b)) / (Γ(c)Γ(a−b)) * (−z)^−b * 2F1(b,b−c+1;b−a+1;1/z)
    This is valid when:
    z∉[0,1]z∈/[0,1]
    arg(−z)arg(−z) is defined (usually −π<arg (−z)<π−π<arg(−z)<π)
    c, a−b, and b−a are not integers to avoid poles in the Gamma functions


"""

from symexpress3 import symexpress3
from symexpress3 import optFunctionBase
from symexpress3 import symtools

class OptSymFunctionHypergeometricToSum( optFunctionBase.OptFunctionBase ):
  """
  Convert cos to e
  """
  def __init__( self ):
    super().__init__()
    self._name         = "hypergeometricToSum"
    self._desc         = "Convert hypergemoetric to sum for abs(z) < 1"
    self._funcName     = "hypergeometric"         # name of the function
    self._minparams    = 3                        # minimum number of parameters
    self._maxparams    = 100                      # maximum number of parameters


  def optimize( self, elem, action ):
    def _transAbsZSmall( valP, valQ, startP, startQ, elemZ ):
      # below transformation is only valid if abs(z) < 1
      try:
        valZ = elemZ.getValue()
        if abs( valZ ) >= 1:
          return None
      except: # pylint: disable=bare-except
        return None


      elemPQ  = symexpress3.SymExpress( '*' )
      varName = symtools.VariableGenerateGet()
      symVarN = symexpress3.SymVariable( varName )

      for iCntVal in range( startP, valP + startP):
        elemA    = elem.elements[ iCntVal ]
        elemFunc = symexpress3.SymFunction( "risingfactorial" )
        elemFunc.add( elemA   )
        elemFunc.add( symVarN )

        elemPQ.add( elemFunc )

      for iCntVal in range( startQ, startQ + valQ):
        elemB    = elem.elements[ iCntVal ]
        elemFunc = symexpress3.SymFunction( "risingfactorial", -1, 1, 1 )
        elemFunc.add( elemB   )
        elemFunc.add( symVarN )

        elemPQ.add( elemFunc )

      elemZExp = symexpress3.SymFunction( "exp" )
      elemZExp.add( symVarN )
      elemZExp.add( elemZ   ) # z^^n

      elemNFact = symexpress3.SymFunction( 'factorial', -1, 1, 1 )
      elemNFact.add( symVarN )

      elemParam = symexpress3.SymExpress( '*' )
      elemParam.add( elemPQ    )
      elemParam.add( elemZExp  )
      elemParam.add( elemNFact )

      elemProduct = symexpress3.SymFunction( 'sum' )
      elemProduct.add( symVarN )
      elemProduct.add( symexpress3.SymNumber( 1, 0, 1, 1, 1, 1, 1 ) )
      elemProduct.add( symexpress3.SymVariable( 'infinity' ))
      elemProduct.add( elemParam )

      elemProduct.powerSign        = elem.powerSign
      elemProduct.powerCounter     = elem.powerCounter
      elemProduct.powerDenominator = elem.powerDenominator

      return elemProduct

    if self.checkType( elem, action ) != True:
      return None

    elemP   = elem.elements[ 0 ]
    elemQ   = elem.elements[ 1 ]

    elemTot = len( elem.elements )
    elemZ   = elem.elements[ elemTot - 1 ]

    if not isinstance( elemP, symexpress3.SymNumber ):
      dVars = elemP.getVariables()
      if len( dVars ) != 0:
        return None
    else:
      if elemP.power != 1:
        return None
      if elemP.factDenominator != 1:
        return None

    if not isinstance( elemQ, symexpress3.SymNumber):
      dVars = elemQ.getVariables()
      if len( dVars ) != 0:
        return None
    else:
      if elemQ.power != 1:
        return None
      if elemQ.factDenominator != 1:
        return None

    try:
      valP = elemP.getValue()
      valQ = elemQ.getValue()
    except: # pylint: disable=bare-except
      return None

    if not isinstance(valP, int):
      return None
    if not isinstance(valQ, int):
      return None

    if valP + valQ + 3 != elemTot:
      return None

    # print( f"Start hyper p:{valP}  q:{valQ}")
    # print( f"function: {str(elem)}")

    # valP = number of p elements
    # valQ = number of q elements

    startP = 2              # first element of p
    startQ = startP + valP  # first element of q

    # multiple solutions
    # 0F0 = e^^z
    # 0F1 = ?
    # 1F0 = (1 - z)^^(-p)
    #
    # 1F1 => integral * 0F0
    # nFm => integral * n(-1)F(m-1)
    #


    # below transformation is only valid if abs(z) < 1
    elemNew = _transAbsZSmall( valP, valQ, startP, startQ, elemZ )
    if elemNew != None:
      return elemNew

    # print( "end hyper nothing to do")
    return None

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symtools.VariableGenerateReset()

  symTest = symexpress3.SymFormulaParser( "hypergeometric( 2, 1, 2, 3, 4, 1/2 )" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  # print( "symTest: " + str( symTest ))

  testClass = OptSymFunctionHypergeometricToSum()
  symNew    = testClass.optimize( symTest, "hypergeometricToSum" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "sum( n1,0,infinity, risingfactorial( 2,n1 ) *  risingfactorial( 3,n1 ) *  risingfactorial( 4,n1 )^^-1 *  exp( n1,(1/2) ) *  factorial( n1 )^^-1 )":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymFunction optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )



if __name__ == '__main__':
  Test( True )
