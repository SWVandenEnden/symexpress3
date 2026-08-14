#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Cos to sum for Sym Express 3

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
# import typing

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncLog
# from symexpress3         import optFunctionBase

class OptSymFunctionLogSplit( symFuncLog.SymFuncLog ): # , optFunctionBase.OptFunctionBase ): -> TypeError: multiple bases have instance lay-out conflict
  """
  Split log into multiple parts
  """
  __slots__ = ( '_funcName',)

  def __init__( self ) -> None :
    super().__init__()
    self._name         = "log"                    # used in functionToValue()
    self._desc         = "Split log into multiple parts, log(2^^3 * 5^^2) = 3log(2)+2log(5)"
    self._funcName     = "log"                    # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 1                        # maximum number of parameters

    self._syntax       = "log(<x> [,<y>])"
    self._synExplain   = "log(<x> [,<y>]), log(2^^3 5^^2) = 3log(2)+2log(5)"
    self._split        = True

  @property
  def functionName(self) -> str:
    """
    Name of the function
    """
    return self._funcName


  # pylint: disable=unused-argument
  def optimize( self, elem:symexpress3.TypVarSym3Object, action:None|str ) -> None|symexpress3.TypVarSym3Object:
    """
    Pass through to functionToValue in symFuncLog.py
    """
    return self.functionToValue( elem )


#
# Test routine (unit test), see testsymexpress3.py -> symFuncLog.py
#
# def Test( display:bool = False) -> None :
#  """
#  Unit test
#  """
#  # pass # see symFuncLog


# if __name__ == '__main__':
#   Test( True )
