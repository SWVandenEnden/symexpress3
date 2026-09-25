#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Abstract class for function implementation symexpress3

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

from abc import ABC, abstractmethod

from symexpress3 import symexpress3

#
# base class for a specific function
#
class SymFuncBase( ABC ):
  """
  Base class for defining a function
  """
  __slots__ = ('_name', '_desc', '_minparams', '_maxparams', '_syntax', '_synExplain' )

  def __init__( self ) -> None:
    self._name         :str      = ""    # must be set by in the real class
    self._desc         :None|str = ""    # description of the function
    self._minparams    :int      = 1     # minimum number of parameters
    self._maxparams    :int      = 1     # maximum number of parameters
    self._syntax       :None|str = None  # syntax of functions: sum(<variable>,<lower>,<upper>,<function>)
    self._synExplain   :None|str = None  # syntax explanation : sum function, from lower to upper, example: sum(n,0,100,exp(x,n)

  @property
  def name(self) -> str:
    """
    Name of the function
    """
    return self._name

  @property
  def description(self) -> None|str :
    """
    Description of the function
    """
    return self._desc

  @property
  def minimumNumberOfParameters(self) -> int :
    """
    Minimum number of parameters
    """
    return self._minparams

  @property
  def maximumNumberOfParameters(self) -> int :
    """
    Maximum number of parameters
    """
    return self._maxparams

  @property
  def syntax(self) -> None|str :
    """
    Syntax of the function
    """
    return self._syntax

  @property
  def syntaxExplain(self) -> None|str :
    """
    More explanation of the syntax (not a description)
    """
    if self._synExplain != None:
      return self._synExplain

    return self._syntax

  @abstractmethod
  def functionToValue( self, elem:symexpress3.TypVarSym3Object ) -> None|symexpress3.TypVarSym3Object :
    """
    Convert a given function into a value/expression.
    Return None if it cannot convert
    """
    return None

  def checkCorrectFunction( self, elem:None|symexpress3.TypVarSym3Object ) -> bool :
    """
    Check if the function is correct (number of parameters, name)
    """
    return self._checkCorrectFunction( elem )

  def _checkCorrectFunction( self, elem:None|symexpress3.TypVarSym3Object ) -> bool :
    # check if the given element is a function and has the correct function name
    # if not isinstance( elem, symexpress3.SymFunction ):
    if elem == None:
      return False

    if elem.classType != symexpress3.CLASSTYPE_SYMFUNCTION :
      return False

    elem = typing.cast( symexpress3.SymFunction, elem )

    if elem.name != self.name:
      return False

    numElem = elem.numElements()
    if  numElem < self._minparams :
      return False
    if numElem > self._maxparams :
      return False

    return True



  def mathMl( self, elem:None|symexpress3.TypVarSym3Object ) -> tuple[list[str], None|str]:
    """
    Give the MathMl string back for the given function
    1e parameter indicate that the power must be done by the caller
    2e parameter is the string MathMl of the function, if None is given back then the caller must do it all
    See symexpress3.SymFunction.MathMl()
    """
    # pylint: disable=unused-argument
    return [], None


  # to be override
  def _getValueSingle( self, dValue:symexpress3.TypVarSym3Value, dValue2:None|symexpress3.TypVarSym3Value = None ) -> symexpress3.TypVarSym3Value :
    # pylint: disable=unused-argument

    # Get a value from a single element
    # pyling do not like none as a return value
    # return None
    return 0

  def _getValueMultiple( self, listOrValue:symexpress3.TypVarSym3ValueAll, listOrValue2:symexpress3.TypVarSym3ValueAll = None ) -> symexpress3.TypVarSym3ValueAll:
    # get value from multiple elements

    listOne = []
    listTwo = []

    singleValue =  True

    if isinstance( listOrValue, list ):
      listOne     = listOrValue
      singleValue = False
    else:
      listOne.append( listOrValue )

    if isinstance( listOrValue2, list ):
      listTwo     = listOrValue2
      singleValue = False
    else:
      listTwo.append( listOrValue2 )

    # just to be sure
    if len( listOne ) == 0:
      listOne.append( None )

    if len( listTwo ) == 0:
      listTwo.append( None )

    result = []
    dValue:symexpress3.TypVarSym3Value = 0
    for valOne in listOne :
      for valTwo in listTwo :
        if valTwo == None:
          dValue = self._getValueSingle( valOne )
        else:
          dValue = self._getValueSingle( valOne, valTwo )
        result.append( dValue )

    if singleValue == False:
      dValue = result

    return dValue   # this is a list or a real/complex value

  def getValue( self, elemFunc:symexpress3.TypVarSym3Object, dDict:symexpress3.TypVarSym3VarDictNone = None ) -> symexpress3.TypVarSym3ValueAll :
    """
    Convert the function into a real/complex value(s)
    """
    if self._checkCorrectFunction( elemFunc ) != True:
      return None

    elemFunc = typing.cast( symexpress3.SymFunction, elemFunc )

    numElem = elemFunc.numElements()
    if numElem < self.minimumNumberOfParameters :
      raise NameError( f'function {elemFunc.name} need {self.minimumNumberOfParameters} parameter found: {numElem}' )

    if numElem > self.maximumNumberOfParameters :
      raise NameError( f'function {elemFunc.name} need at most {self.maximumNumberOfParameters} parameters found: {numElem}' )

    if numElem > 2:
      raise NameError( 'function {elemFunc.name} more as 2 parameters no automatic supported at the moment' )

    if numElem >= 2:
      listOrValue1 = elemFunc.elements[ 0 ].getValue( dDict )
      listOrValue2 = elemFunc.elements[ 1 ].getValue( dDict )

      listOrValue = self._getValueMultiple( listOrValue1, listOrValue2 )
      listOrValue = typing.cast( symexpress3.TypVarSym3ValueList, listOrValue )

      listOrValue = elemFunc.valuePow( listOrValue )
    else:
      listOrValue = elemFunc.elements[ 0 ].getValue( dDict )
      listOrValue = self._getValueMultiple( listOrValue )
      listOrValue = typing.cast( symexpress3.TypVarSym3ValueList, listOrValue )
      listOrValue = elemFunc.valuePow( listOrValue )

    return listOrValue

  def getVarname( self, elemVar:symexpress3.TypVarSym3Object ) -> None|str :
    """
    Get the variable name of given expression
    Special for integral functions
    """

    # while elemVar != None and not isinstance( elemVar, symexpress3.SymVariable):
    while elemVar.classType != symexpress3.CLASSTYPE_SYMVARIABLE :
      if elemVar.power != 1:
        # elemVar = None
        return None

      # elif isinstance( elemVar, symexpress3.SymExpress ):
      if elemVar.classType == symexpress3.CLASSTYPE_SYMEXPRESS :
        elemVar = typing.cast( symexpress3.SymExpress, elemVar )
        if elemVar.numElements() == 1:
          elemVar = elemVar.elements[0]
        else:
          # elemVar = None
          return None

      else:
        # elemVar = None
        return None

    # if not isinstance( elemVar, symexpress3.SymVariable):
    if elemVar.classType != symexpress3.CLASSTYPE_SYMVARIABLE :
      return None

    if elemVar.power != 1:
      return None

    elemVar = typing.cast( symexpress3.SymVariable, elemVar )
    cVar = elemVar.name

    return cVar
