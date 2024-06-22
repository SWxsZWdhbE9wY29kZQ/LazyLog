#!/usr/bin/env python3
#	log.py - Python 3.4.x
#	Copyright © 2018, Leiah Grace
#
#	GPLv3 License:
#	This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
#	Public License as published by the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#	implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
#	License for more details.
#
#	You should have received a copy of the GNU General Public License along with this program. If not,
#	see <http://www.gnu.org/licenses/>.
#
#	Usage:
#		Log = Log()
#			- Make an unnamed new Log instance that will log all data to terminal, with no file output
#		Log = Log("LogInstance", Log.Level.VERBOSE, Log.Level.VERBOSE, './LogFile.log')
#			- Make a new Log instance named "LogInstance" that will log all data to terminal and 'LogFile.log'
#		Additionally, after first instantiation further instances of Log will automatically retrieve their
# 		configuration from values set on the LogManager singleton, meaning all the modules in a project will
# 		all log the same way (and to the same file) without needing to be set on each module. This behaviour
# 		can be overridden by setting the log levels and path manually on an instance
# === Imports ===
import os.path as path
from enum import IntEnum
from time import localtime, strftime

# === Interface Classes ===
class LogManager():
	_termLogLevel = None
	_fileLogLevel = None
	_fileLogPath = None

	def __new__(cls) -> object:
		if not hasattr(cls, 'instance'):
			cls.instance = super(LogManager, cls).__new__(cls)
		
		return cls.instance
class Log():
	class Level(IntEnum):
		VERBOSE = 0
		DEBUG = 1
		INFO = 2
		WARNING = 3
		ERROR = 4
		CRITICAL = 5
		DISABLED = 6
	class Format():
		class FG():
			def Black(string) -> str:
				return "\033[30m{0}\033[0m".format(string)
			def Red(string) -> str:
				return "\033[31m{0}\033[0m".format(string)
			def Green(string) -> str:
				return "\033[32m{0}\033[0m".format(string)
			def Yellow(string) -> str:
				return "\033[33m{0}\033[0m".format(string)
			def Blue(string) -> str:
				return "\033[34m{0}\033[0m".format(string)
			def Magenta(string) -> str:
				return "\033[35m{0}\033[0m".format(string)
			def Cyan(string) -> str:
				return "\033[36m{0}\033[0m".format(string)
			def White(string) -> str:
				return "\033[37m{0}\033[0m".format(string)
			def BrightBlack(string) -> str:
				return "\033[90m{0}\033[0m".format(string)
			def BrightRed(string) -> str:
				return "\033[91m{0}\033[0m".format(string)
			def BrightGreen(string) -> str:
				return "\033[92m{0}\033[0m".format(string)
			def BrightYellow(string) -> str:
				return "\033[93m{0}\033[0m".format(string)
			def BrightBlue(string) -> str:
				return "\033[94m{0}\033[0m".format(string)
			def BrightMagenta(string) -> str:
				return "\033[95m{0}\033[0m".format(string)
			def BrightCyan(string) -> str:
				return "\033[96m{0}\033[0m".format(string)
			def BrightWhite(string) -> str:
				return "\033[97m{0}\033[0m".format(string)
		class BG():
			def Black(string) -> str:
				return "\033[40m{0}\033[0m".format(string)
			def Red(string) -> str:
				return "\033[41m{0}\033[0m".format(string)
			def Green(string) -> str:
				return "\033[42m{0}\033[0m".format(string)
			def Yellow(string) -> str:
				return "\033[43m{0}\033[0m".format(string)
			def Blue(string) -> str:
				return "\033[44m{0}\033[0m".format(string)
			def Magenta(string) -> str:
				return "\033[45m{0}\033[0m".format(string)
			def Cyan(string) -> str:
				return "\033[46m{0}\033[0m".format(string)
			def White(string) -> str:
				return "\033[47m{0}\033[0m".format(string)
			def BrightBlack(string) -> str:
				return "\033[100m{0}\033[0m".format(string)
			def BrightRed(string) -> str:
				return "\033[101m{0}\033[0m".format(string)
			def BrightGreen(string) -> str:
				return "\033[102m{0}\033[0m".format(string)
			def BrightYellow(string) -> str:
				return "\033[103m{0}\033[0m".format(string)
			def BrightBlue(string) -> str:
				return "\033[104m{0}\033[0m".format(string)
			def BrightMagenta(string) -> str:
				return "\033[105m{0}\033[0m".format(string)
			def BrightCyan(string) -> str:
				return "\033[106m{0}\033[0m".format(string)
			def BrightWhite(string) -> str:
				return "\033[107m{0}\033[0m".format(string)
		def Bold(string) -> str:
			return "\033[1m{0}\033[0m".format(string)
		def Faint(string) -> str:
			return "\033[2m{0}\033[0m".format(string)
		def Italic(string) -> str:
			return "\033[3m{0}\033[0m".format(string)
		def Underline(string) -> str:
			return "\033[4m{0}\033[0m".format(string)
		def SlowBlink(string) -> str:
			return "\033[5m{0}\033[0m".format(string)
		def RapidBlink(string) -> str:
			return "\033[6m{0}\033[0m".format(string)
		def Reverse(string) -> str:
			return "\033[7m{0}\033[0m".format(string)
		def Conceal(string) -> str:
			return "\033[8m{0}\033[0m".format(string)
		def StrikeThrough(string) -> str:
			return "\033[9m{0}\033[0m".format(string)
	
	def __init__(self, loggerName=None, termLogLevel=None, fileLogLevel=None, fileLogPath=None) -> None:
		self._initialised = False
		self._manager = LogManager()

		# Set the logger name. We parse it as a string first, to avoid any potential bugs
		if loggerName is not None:
			self._loggerName = "{0}:".format(str(loggerName))
		else:
			self._loggerName = ""
		
		# Set the log level for the terminal and file output
		if termLogLevel is not None:
			self._termLogLevel = termLogLevel

			if self._manager._termLogLevel is None:
				self._manager._termLogLevel = termLogLevel
		elif self._manager._termLogLevel is not None:
			self._termLogLevel = self._manager._termLogLevel
		else:
			self._termLogLevel = Log.Level.VERBOSE
		if fileLogLevel is not None:
			self._fileLogLevel = fileLogLevel

			if self._manager._fileLogLevel is None:
				self._manager._fileLogLevel = fileLogLevel
		elif self._manager._fileLogLevel is not None:
			self._fileLogLevel = self._manager._fileLogLevel
		else:
			self._fileLogLevel = Log.Level.DISABLED

		# Validate the file output path  NOTE: to avoid a race condition, we need to recheck this again before actually writing to the file
		if fileLogPath is not None:
			isFile = path.isfile(fileLogPath)

			try:
				with open(fileLogPath, 'a') as f:
					if isFile:
						f.write("\n") # Add an empty line at the end of the log file if we're appending, otherwise we basically just touch the file
			except IOError:
				raise Exception("Invalid filepath or incorrect permissions on file \'{0}\'".format(fileLogPath))
			finally:
				self._fileLogPath = fileLogPath

				if self._manager._fileLogPath is None:
					self._manager._fileLogPath = fileLogPath
		elif self._manager._fileLogPath is not None:
			self._fileLogPath = self._manager._fileLogPath
		else:
			self._fileLogLevel = Log.Level.DISABLED
		
		self._initialised = True

	def Print(self, string) -> None:
		if self._initialised:
			self._logToTerminal(string)
		else:
			raise Exception("Log Interface hasn't been initialised")
	def Verbose(self, string) -> None:
		if self._initialised:
			if self._termLogLevel <= Log.Level.VERBOSE:
				self._logToTerminal("{0} {1}VERBOSE: {2}".format(self._shortTime(), self._loggerName, string))
			if self._fileLogLevel <= Log.Level.VERBOSE:
				self._logToFile("{0} {1}VERBOSE: {2}".format(self._longTime(), self._loggerName, string))
		else:
			raise Exception("Log Interface hasn't been initialised")
	def Debug(self, string) -> None:
		if self._initialised:
			if self._termLogLevel <= Log.Level.DEBUG:
				self._logToTerminal("{0} {1}".format(Log.Format.FG.BrightGreen("{0} {1}DEBUG:".format(self._shortTime(), self._loggerName)), string))
			if self._fileLogLevel <= Log.Level.DEBUG:
				self._logToFile("{0} {1}DEBUG: {2}".format(self._longTime(), self._loggerName, string))
		else:
			raise Exception("Log Interface hasn't been initialised")
	def Info(self, string) -> None:
		if self._initialised:
			if self._termLogLevel <= Log.Level.INFO:
				self._logToTerminal("{0} {1}".format(Log.Format.FG.BrightCyan("{0} {1}INFO:".format(self._shortTime(), self._loggerName)), string))
			if self._fileLogLevel <= Log.Level.INFO:
				self._logToFile("{0} {1}INFO: {2}".format(self._longTime(), self._loggerName, string))
		else:
			raise Exception("Log Interface hasn't been initialised")
	def Warning(self, string) -> None:
		if self._initialised:
			if self._termLogLevel <= Log.Level.WARNING:
				self._logToTerminal("{0} {1}".format(Log.Format.FG.BrightYellow("{0} {1}WARNING:".format(self._shortTime(), self._loggerName)), string))
			if self._fileLogLevel <= Log.Level.WARNING:
				self._logToFile("{0} {1}WARNING: {2}".format(self._longTime(), self._loggerName, string))
		else:
			raise Exception("Log Interface hasn't been initialised")
	def Error(self, string) -> None:
		if self._initialised:
			if self._termLogLevel <= Log.Level.ERROR:
				self._logToTerminal("{0} {1}".format(Log.Format.FG.Red("{0} {1}ERROR:".format(self._shortTime(), self._loggerName)), string))
			if self._fileLogLevel <= Log.Level.ERROR:
				self._logToFile("{0} {1}ERROR: {2}".format(self._longTime(), self._loggerName, string))
		else:
			raise Exception("Log Interface hasn't been initialised")
	def Critical(self, string) -> None:
		if self._initialised:
			if self._termLogLevel <= Log.Level.CRITICAL:
				self._logToTerminal("{0} {1}".format(Log.Format.BG.Red(Log.Format.FG.Black("{0} {1}CRITICAL:".format(self._shortTime(), self._loggerName))), string))
			if self._fileLogLevel <= Log.Level.CRITICAL:
				self._logToFile("{0} {1}CRITICAL: {2}".format(self._longTime(), self._loggerName, string))
		else:
			raise Exception("Log Interface hasn't been initialised")

	def _logToTerminal(self, string) -> None:
		print(string)
	def _logToFile(self, string) -> None:
		if self._fileLogLevel is not Log.Level.DISABLED:
			try:
				with open(self._fileLogPath, 'a') as f:
					f.write(string + "\n")
			except IOError as error:
				raise Exception("Invalid filepath or incorrect permissions on file \'{0}\'".format(self._fileLogPath))
	def _shortTime(self) -> str:
		return strftime("[%H:%M:%S]", localtime())
	def _longTime(self) -> str:
		return strftime("[%Y/%m/%d %H:%M:%S]", localtime())