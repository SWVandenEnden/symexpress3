#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (C) 2021 Gien van den Enden - swvandenenden@gmail.com

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

# This import give cyclic-import warnings (pylint) we need some sort of forward declaration

# from symexpress3          import optTypeBase
# from symexpress3          import optFunctionBase
# from symexpress3.optimize import optimizeBase
# from symexpress3.symfunc  import symFuncBase

# Different between functionTable and optSymFunction is functionTable can calculate a value from a function, optSymFunction cannot
# functionTable       :dict[str,symFuncBase.SymFuncBase        ] = {} # dictionary of functions of type SymFuncBase     , see symexpress3.symfunc.symRegisterFunctions
# optimizeTable       :dict[str,optimizeBase.OptimizeBase      ] = {} # dictionary of optimize classes for SymExpress   , see symexpress3.optimize.symRegisterOptimze
# optSymNumberTable   :dict[str,optTypeBase.OptTypeBase        ] = {} # dictionary of optimize classes for SymNumber
# optSymVariableTable :dict[str,optTypeBase.OptTypeBase        ] = {} # dictionary of optimize classes for SymVariable
# optSymFunctionTable :dict[str,optFunctionBase.OptFunctionBase] = {} # dictionary of optimize classes for SymFunction
# optSymAnyTable      :dict[str,optTypeBase.OptTypeBase        ] = {} # dictionary of optimize classes for any type, last resort if the optimize not fit in 1 of the above

functionTable       :dict[str,typing.Any ] = {} # dictionary of functions of type SymFuncBase     , see symexpress3.symfunc.symRegisterFunctions
optimizeTable       :dict[str,typing.Any ] = {} # dictionary of optimize classes for SymExpress   , see symexpress3.optimize.symRegisterOptimze
optSymNumberTable   :dict[str,typing.Any ] = {} # dictionary of optimize classes for SymNumber
optSymVariableTable :dict[str,typing.Any ] = {} # dictionary of optimize classes for SymVariable
optSymFunctionTable :dict[str,typing.Any ] = {} # dictionary of optimize classes for SymFunction
optSymAnyTable      :dict[str,typing.Any ] = {} # dictionary of optimize classes for any type, last resort if the optimize not fit in 1 of the above


fixedVariables      :dict[str,str                            ] = {} # dictionary of fixed variables, see symtools.py


# def RegisterTableEntry( cType:str, oEntry:optTypeBase.OptTypeBase|optFunctionBase.OptFunctionBase|optimizeBase.OptimizeBase ):
def RegisterTableEntry( cType:str, oEntry:typing.Any ) -> None :
  """
  Register the given optimize class
  """

  # pylint: disable=multiple-statements
  if   cType == "optSymNumber"   :  optSymNumberTable[   oEntry.name ] = oEntry
  elif cType == "optSymVariable" :  optSymVariableTable[ oEntry.name ] = oEntry
  elif cType == "optSymFunction" :  optSymFunctionTable[ oEntry.name ] = oEntry
  elif cType == "optimize"       :  optimizeTable[       oEntry.name ] = oEntry
  elif cType == "function"       :  functionTable[       oEntry.name ] = oEntry
  elif cType == "optSymAny"      :  optSymAnyTable[      oEntry.name ] = oEntry
  else:
    raise NameError( f'RegisterTableEntry, unknown type: {cType}' )
