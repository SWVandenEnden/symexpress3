#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Command line interface for Symbolic expression 3

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

import sys
import os

from pathlib import Path

import mpmath       # type: ignore
import symexpress3

from symexpress3 import version


def TextOutput( cText:str, cFileName:None|str ) -> None:
  """
  Output text to the given filename. No filename given output to stdout
  """
  if cFileName != None:
    with open( cFileName, mode="a", encoding="utf-8") as f:
      f.write( cText + '\n' )
  else:
    print( cText )


def OptimzeFunction( cExpress:str, outputFormat:str|list[str], optimizeActions:list[str], exportFile:None|str ) -> None:
  """
  Optimize the given expression according the optimize actions
  Output the result for the given output types`
  """
  # import pudb; pudb.set_trace()

  # convert string expression into object
  try:
    oExpress = symexpress3.SymFormulaParser( cExpress )
  except NameError as exceptInfo:
    print( "Error in expression: " + cExpress )
    print( exceptInfo )
    return
  except:  # pylint: disable=bare-except
    print( "Error in expression: " + cExpress )
    print( str( sys.exc_info()[0] ))
    return

  # optimize expression
  if len( optimizeActions ) < 1:
    oExpress.optimizeExtended()
  else:
    oExpress.optimize()
    for optKey in optimizeActions:
      if optKey == "optimizeNormal":
        oExpress.optimizeNormal()
        continue
      if optKey == "optimizeExtended":
        oExpress.optimizeExtended()
        continue
      if optKey == "none":
        oExpress.optimize()
        continue
      oExpress.optimize( optKey )
      oExpress.optimize()


  if exportFile != None:
    try:
      os.remove(exportFile)
    except OSError:
      pass

  # output expression
  if outputFormat == "":
    TextOutput( str( oExpress ), exportFile  )
  else:
    for outputType in outputFormat:
      if outputType == "c":
        try:
          dValue = oExpress.getValue()
          TextOutput( str( dValue ), exportFile  )
        except NameError as exceptInfo:
          print( "Error in getting the value of expression: " + cExpress )
          print( exceptInfo )
          return

      elif outputType == "s":
        TextOutput( str( oExpress ), exportFile  )

      elif outputType == "m":
        TextOutput( oExpress.mathMl(), exportFile  )

      elif outputType == "h":
        output = symexpress3.SymToHtml( exportFile, "SymExpress 3" )
        # try:
        output.writeSymExpress( oExpress )
        output.writeLine( str( oExpress ))

        # except:
        #  pass

        output.closeFile()

      elif outputType == "t":
        if exportFile != None:
          with open( exportFile, mode="a", encoding="utf-8") as f:
            symexpress3.SymExpressTree( oExpress, f )
        else:
          symexpress3.SymExpressTree( oExpress )

      else:
        print( "Unknown output (-o) : {outputType}" )
        return # stop by unknown output`



def CheckOptimizeActions( cList:str ) -> list[str]:
  """
  Check of the given optimize actions are valid
  """
  optDict = symexpress3.GetAllOptimizeActions()

  actions = cList.split(",")
  actions = [s.strip() for s in actions]

  for optKey in actions:

    if optKey == "optimizeNormal":
      continue

    if optKey == "optimizeExtended":
      continue

    if optKey == "none":
      continue

    if optKey in optDict:
      continue

    print( f"Unknown optimize action (-a) : {optKey}" )

  return actions


def DisplayList( listTypes:str ) -> None:
  """
  Display list of the given type
  f = functions
  a = optimize actions
  v = fixed variables
  """
  for listType in listTypes:
    if listType == "f" :
      print( "Functions:" )
      funcTable = symexpress3.GetAllFunctions()
      funcTable = dict(sorted(funcTable.items()))

      for optKey, optValue in funcTable.items():
        print( f"  {optKey: <30} - {optValue}" )

    elif listType == "a" :
      print( "Optimize actions:")
      optDict = symexpress3.GetAllOptimizeActions()
      optDict = dict(sorted(optDict.items()))

      optDict[ "optimizeNormal"   ] = "Normal optimization"
      optDict[ "optimizeExtended" ] = "Extended optimization"
      optDict[ "none"             ] = "Optimize internal structure"

      for optKey, optValue in optDict.items():
        print( f"  {optKey: <30} - {optValue}" )

    elif listType == "v" :
      print( "Predefined variables:" )
      varDict = symexpress3.GetFixedVariables()
      for varKey, varValue in varDict.items():
        print( f"  {varKey: <8} - {varValue}" )

    else:
      print( f"Unknown -list options: {listType}" )

def DisplayVersion() -> None:
  """
  Display version information
  """
  # print( "symexp3cmd.py - symexpress3 command line interface" )
  print( "Version    : " + version.__version__    )
  # print( "Build number: " + symexpress3.symexpress3.__buildnumber__ )

  # print( "Author     : " + version.__author__     )
  print( "Copyright  : " + version.__copyright__  )
  print( "License    : " + version.__license__    )
  # print( "Maintainer : " + version.__maintainer__ )
  print( "Email      : " + version.__email__      )
  print( "Status     : " + version.__status__     )


def DisplayHelp() -> None:
  """
  Display help
  """
  # print( "symexp3cmd.py - symexpress3 command line interface" )
  # print( "usage: symexp3cmd [options] [arg] " )
  print( "usage: python -m symexpress3 [options] [arg]" )
  print( "options: " )
  print( "  -h           : Help" )
  print( "  -v           : Version information" )
  print( "  -a <actions> : Comma separated list of actions" )
  print( "  -l <types>   : List of types" )
  print( "                 f = defined functions" )
  print( "                 a = optimize actions" )
  print( "                 v = fixed variables" )
  print( "  -o <format>  : Output format" )
  print( "                 s - string format (default)" )
  print( "                 m - MathML (xml) format" )
  print( "                 c - Calculated value " )
  print( "                 t - tree view" )
  print( "                 h - html, formula in string and MathMl format" )
  print( "  -e <file>    : Output file" )
  print( "  -f <file>    : Read formula from text file instead of the command line" )
  print( "  -dps <number>: Calculation precision, default is 20" )
  print( " " )
  print( "arg:" )
  print( "<formula>" )
  print( " " )
  print( "Example: " )
  print( 'python -m symexpress3 -v -l fav -o sc "cos( pi / 4 )^^(1/3)"' )

def CommandLine( argv:list[str] ) -> None:
  """
  Process the symexpres3 command line parameters
  """
  outputFormat        = ""
  exportFile:None|str = None
  optimizeActions     = []

  mpmath.mp.dps = 20 # precision for calculations, https://mpmath.org/doc/current/basics.html

  nrarg = len( argv )

  # nothing given, then display help
  if nrarg <= 1:
    DisplayHelp()

  mode        = ""
  expressions = []

  for iCnt in range( 1, nrarg ) :
    cArg = argv[ iCnt ]

    match mode :
      case "file":
        data = Path( cArg ).read_text( encoding="utf-8" )
        expressions.append( data )

      case "list"      : DisplayList( cArg )
      case "exportfile": exportFile      = cArg
      case "output"    : outputFormat    = cArg
      case "optimize"  : optimizeActions = CheckOptimizeActions( cArg )
      case "precision" : mpmath.mp.dps   = int( cArg )

    if mode != "":
      mode = ""
      continue

    match cArg:
      case "-h"  : DisplayHelp()
      case "-v"  : DisplayVersion()
      case "-l"  : mode = "list"
      case "-o"  : mode = "output"
      case "-a"  : mode = "optimize"
      case "-f"  : mode = "file"
      case "-e"  : mode = "exportfile"
      case "-dps": mode = "precision"
      case _:
        if cArg.startswith( "-" ):
          print( f"Unknown option: {cArg}, use -h for help")
        else:
          # collect the given expression, process after all the options are read
          expressions.append( cArg )

  # process all the given expressions
  for key in expressions:
    OptimzeFunction( key, outputFormat, optimizeActions, exportFile )


# ---------------------------
# The end
# ---------------------------
