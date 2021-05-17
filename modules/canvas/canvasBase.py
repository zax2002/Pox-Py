from modules.canvas.complexColors import ComplexColors

import os
import sys
import threading

try:
	import cursor
except ModuleNotFoundError:
	cursor = None

class CanvasBase:
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.data = {}
		self.buffer = {}
		self.textBuffer = ""

		self.defaultForeColor = self.currentForeColor = self.cursorForeColor = ComplexColors.WHITE[0]
		self.defaultBackColor = self.currentBackColor = self.cursorBackColor = ComplexColors.BLACK[1]

		self.cursorPos = (0, 0)

		self.semiCharEmpty  = " "
		self.semiCharTop 	= "▀"
		self.semiCharBottom = "▄"
		self.semiCharFull 	= "█"

		self.lock = threading.Lock()

	def init(self):
		self.resizeWindow(self.width, self.height)
		self.clear()
		self._print(self.cursorForeColor+self.cursorBackColor)

	def resizeWindow(self, width, height):
		if os.name == "nt":
			os.system(f"mode {width},{height}")
		elif os.name == "posix":
			sys.stdout.write(f"\x1b[8;{height};{width}t")

	def clear(self):
		if os.name == "nt":
			os.system("cls")
		elif os.name == "posix":
			sys.stdout.write("clear")

	def char(self, x, y, char, foreColor=None, backColor=None, standalone=True):
		with self.lock:

			if standalone:
				if x < 0 or x >= self.width or y < 0 or y >= self.height:
					return

				if foreColor == None:
					foreColor = self.currentForeColor
				else:
					self.currentForeColor = foreColor

				if backColor == None:
					backColor = self.currentBackColor
				else:
					self.currentBackColor = backColor
			
			self.buffer[(x, y)] = [False, char, foreColor, backColor]

	def semiPixel(self, x, semiY, complexColor=None, standalone=True):
		y = semiY // 2
		half = semiY % 2

		with self.lock:

			if standalone:
				if x < 0 or x >= self.width or y < 0 or y >= self.height:
					return

				if complexColor == None:
					complexColor = ComplexColors.fromForeColor(self.currentForeColor)
				else:
					self.currentForeColor = complexColor[0]

			if (x, y) in self.buffer and self.buffer[(x, y)][0]:
				currentValue = self.buffer[(x, y)]
			else:
				currentValue = [True, None, None]
			currentValue[1 + half] = complexColor
			self.buffer[(x, y)] = currentValue

	def render(self):
		with self.lock:

			for coordinates, value in self.buffer.items():
				currentValue = self.data[coordinates] if coordinates in self.data else None

				# semi pixel
				if value[0]:
					newTopComplexColor, newBottomComplexColor = value[1:]

					if currentValue != None:
						if currentValue[0]:
							currentForeColor, currentBackColor, currentTopSet, currentBottomSet = currentValue[1:]

							# nothing to change
							if (newTopComplexColor == None or (currentTopSet and newTopComplexColor[0] == currentForeColor) or (not currentTopSet and newTopComplexColor[1] == currentBackColor)) and (newBottomComplexColor == None or (currentBottomSet and newBottomComplexColor[0] == currentForeColor) or (not currentBottomSet and newBottomComplexColor[1] == currentBackColor)):
								continue
						else:
							currentForeColor, currentBackColor, currentTopSet, currentBottomSet = currentValue[2:] + [False, False]
					else:
						currentForeColor, currentBackColor, currentTopSet, currentBottomSet = self.defaultForeColor, self.defaultBackColor, False, False


					if newTopComplexColor == None:
						if currentTopSet:
							newTopComplexColor = ComplexColors.fromForeColor(currentForeColor)
						else:
							newTopComplexColor = ComplexColors.fromBackColor(currentBackColor)

					elif newBottomComplexColor == None:
						if currentBottomSet:
							newBottomComplexColor = ComplexColors.fromForeColor(currentForeColor)
						else:
							newBottomComplexColor = ComplexColors.fromBackColor(currentBackColor)

					# newTop == newBottom
					if newTopComplexColor == newBottomComplexColor:
						if newTopComplexColor[0] == self.cursorForeColor:
							self._printAt(*coordinates, self.semiCharFull)

							self.data[coordinates] = [True, self.cursorForeColor, self.cursorBackColor, True, True]
						else:
							if newTopComplexColor[1] != self.cursorBackColor:
								self._setBackColor(newTopComplexColor[1])

							self._printAt(*coordinates, self.semiCharEmpty)

							self.data[coordinates] = [True, self.cursorForeColor, self.cursorBackColor, False, False]

					# newTop != newBottom
					else:
						# topColor == curForeColor
						if newTopComplexColor[0] == self.cursorForeColor:
							if newBottomComplexColor[1] != self.cursorBackColor:
								self._setBackColor(newBottomComplexColor[1])

							self._printAt(*coordinates, self.semiCharTop)

							self.data[coordinates] = [True, self.cursorForeColor, self.cursorBackColor, True, False]

						# bottomColor == curForeColor
						elif newBottomComplexColor[0] == self.cursorForeColor:
							if newTopComplexColor[1] != self.cursorBackColor:
								self._setBackColor(newTopComplexColor[1])

							self._printAt(*coordinates, self.semiCharBottom)

							self.data[coordinates] = [True, self.cursorForeColor, self.cursorBackColor, False, True]

						# topColor == curBackColor
						elif newTopComplexColor[1] == self.cursorBackColor:
							self._setForeColor(newBottomComplexColor[0])
							self._printAt(*coordinates, self.semiCharBottom)

							self.data[coordinates] = [True, self.cursorForeColor, self.cursorBackColor, False, True]

						# bottomColor == curBackColor
						elif newBottomComplexColor[1] == self.cursorBackColor:
							self._setForeColor(newTopComplexColor[0])
							self._printAt(*coordinates, self.semiCharTop)

							self.data[coordinates] = [True, self.cursorForeColor, self.cursorBackColor, True, False]

						# topColor != curForeColor and bottomColor != curForeColor & topColor != curBackColor & bottomColor != curBackColor
						else:
							self._setForeColor(newTopComplexColor[0])
							self._setBackColor(newBottomComplexColor[1])
							self._printAt(*coordinates, self.semiCharTop)

							self.data[coordinates] = [True, self.cursorForeColor, self.cursorBackColor, True, False]

				# regular char
				else:
					char, foreColor, backColor = value[1:]

					if currentValue == None or currentValue[0]:
						currentValue = [False, " ", self.defaultForeColor, self.defaultBackColor]

					currentChar, currentForeColor, currentBackColor = currentValue[1:]

					if char == currentChar and foreColor == currentForeColor and backColor == currentBackColor:
						continue

					self._setForeColor(foreColor)
					self._setBackColor(backColor)
					self._printAt(*coordinates, char)

					self.data[coordinates] = value

			self.buffer = {}

			self._flushText()

	def hideCursor(self):
		if cursor:
			cursor.hide()

	def showCursor(self):
		if cursor:
			cursor.show()

	def _printAt(self, x, y, string):
		self._setCursor(x, y)
		self._print(string)

	def _setCursor(self, x, y):
		# if self.cursorPos == (x, y):
		# 	return

		# self.cursorPos = (x, y)
		self._print(f"\x1b[{y+1};{x+1}f")

	def _setForeColor(self, color):
		if self.cursorForeColor == color:
			return

		self.cursorForeColor = color
		self._print(color)

	def _setBackColor(self, color):
		if self.cursorBackColor == color:
			return

		self.cursorBackColor = color
		self._print(color)

	def _print(self, string):
		self.textBuffer += string

	def _flushText(self):
		sys.stdout.write(self.textBuffer)
		sys.stdout.flush()
		self.textBuffer = ""


	def _debug(self, *data):
		with open("./debug.log", "a") as f:
			f.write(f"{data}\n")