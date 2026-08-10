#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Prime Factorization

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


    https://stackoverflow.com/questions/32871539/integer-Factorization-in-python
    https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm

"""

import flint # prime factorization, https://github.com/flintlib/python-flint


globalCachePrimeFactors :dict[int,dict[int,int]] = {}
globalCacheDivisors     :dict[int,list[int]]     = {}
globalMaxDigits         :int                     = 60 # 90 # max number of digits for factorization


#
# factor all positive numbers (prime factors)
#
def FactorizationDict(n:int) -> dict[int,int]:
  """
  Factorization given number into prime numbers, give dictionary back ( number: count )
  """
  # global globalCachePrimeFactors

  # print( f"FactorizationDict n: {n}  {type(n)}")
  # n = int( n )
  if n in globalCachePrimeFactors:
    # print( f"FactorizationDict cache used {n} : {globalCachePrimeFactors[ n ]}")
    return globalCachePrimeFactors[ n ].copy()

  factorDict = {}
  if n in( 1, 2, 3, 5, 7, 11, 13 ) :
    factorDict[ n ] = 1
  else:
    # https://en.wikipedia.org/wiki/List_of_prime_numbers
    lowPrimeList = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    # lowPrimeList = [2]

    splitNumber = n
    for primeWalk in lowPrimeList :

      if n < primeWalk:
        break

      modRest = splitNumber % primeWalk
      while modRest == 0:
        factorDict.setdefault(primeWalk, 0)
        factorDict[ primeWalk ] += 1

        splitNumber //= primeWalk
        modRest = splitNumber % primeWalk

    # number not factorized, to big to do it
    if splitNumber > 1:
      if len( str( splitNumber )) > globalMaxDigits:
        factorDict[ splitNumber ] = 1
      else:
        # factorDict += sympy.ntheory.factorint( n )

        factorList = flint.fmpz( n ).factor()
        for fact in factorList:
          factorDict[ int(fact[0]) ] = int(fact[1])

        # factorDict = factorDict | sympy.ntheory.factorint( splitNumber )
        # sympy (mpmath) give gmpy2 integers back, but I want Python integers
        # factorDict = {int(key):int(value) for ( key, value ) in factorDict.items()}

  globalCachePrimeFactors[ n ] = factorDict.copy()

  # print( f'After factorDict, count: { len(globalCachePrimeFactors)}' )

  return factorDict


# get all the factors (divisors) of the given n`
def Divisors( n:int ) -> list[int] :
  """
  Get all the divisors (factors) of a given n
  """

  n = abs( n )

  if n in globalCacheDivisors:
    return globalCacheDivisors[ n ].copy()

  factPrime = FactorizationDict( n  )
  primeKeys = sorted(factPrime.keys())
  lenKeys   = len( primeKeys )

  def NextDivisor( nPrimePos:int ) -> list[int]:

    # no more primes
    if nPrimePos >= lenKeys:
      return [1]

    # all the powers of the prime
    powers = [1]

    primeNr  = primeKeys[ nPrimePos ]
    cntPrime = factPrime[ primeNr ]

    # for iPowers in range( cntPrime ):
    for _ in range( cntPrime ):
      # powers.append(  primeNr ** ( iPowers + 1))
      powers.append(  powers[-1] * primeNr )

    # get all the next divisors
    iNumbers = NextDivisor( nPrimePos + 1 )
    result = []

    # add current prime to the list
    for iNumber in iNumbers :
      for iPower in powers :
        # print( f"iNumber: {iNumber}, iPower: {iPower}, nPrimePos: {nPrimePos}")
        newNumber = iNumber * iPower
        result.append(  newNumber )

    return result


  factors = NextDivisor( 0 ) # get all divisors
  # Make unique and sorted
  factors = sorted(list(set( factors )))


  # factors = sympy.divisors( n )

  # force Python integers sympy give gmpy2 integers
  # factors = [ int(key) for key in factors ]


  globalCacheDivisors[ n ] = factors.copy()

  # print( f"Divisors done: {n}  count: { len(globalCacheDivisors[ n ]) }" )

  return factors
