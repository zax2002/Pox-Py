from modules.canvas.canvas import Canvas
from modules.canvas.complexColors import ComplexColors

import time
import random
import threading

from pynput import keyboard

class Tetris:
	def __init__(self):
		self.canvas = Canvas(27, 12)

		self._loadFigures(
			( "██",   ComplexColors.GREEN 		),
			
			( "▀▀▀▀", ComplexColors.LIGHT_GREEN	),

			( "█▄▄",  ComplexColors.CYAN		),

			( "▄▄█",  ComplexColors.LIGHT_BLUE	),

			( "▄█▄",  ComplexColors.YELLOW		),

			( "▄█▀",  ComplexColors.LIGHT_RED   ),

			( "▀█▄",  ComplexColors.RED 	  	)
		)

		self.fieldPosition = (2, 2)
		self.fieldSize = (10, 20)
		self.nextFigurePosition = (15, 2)

		self.canvas.init()
		self.canvas.hideCursor()

		self.drawInterface()
		self.canvas.render()

		self.lock = threading.Lock()
		self.gameIsOn = False

		with keyboard.Listener(on_press=self.onKeyPress) as thread:
			self.listenerThread = thread
			self.listenerThread.join()

	def start(self):
		# raise NotImplementedError

		self.gameIsOn = True

		with self.lock:
			self.field = {}

			self.fallingFigure = None
			self.fallingFigureLocalPosition = None
			self.nextFigure = None

			self.score = 0
			self.lines = 0
			self.level = 1

			self.interval = 0.5 / 1.1

			self.spawnFigure()

			self.drawField()
			self.drawFallingFigure()
			self.drawNextFigure()
			self.drawScore()

		threading.Thread(target=self.ticking).start()
		
	def ticking(self):
		while self.gameIsOn:
			self.moveDown()

			time.sleep(self.interval)

	def gameOver(self):
		# raise NotImplementedError

		self.gameIsOn = False

		print("Game Over")

	# Controls ------------------------------------------------------------------------------------

	def onKeyPress(self, key):
		if key == keyboard.Key.esc:
			self.listenerThread.stop()
			exit()

		elif not self.gameIsOn:
			if key == keyboard.Key.space:
				self.start()

		elif key == keyboard.Key.up:
			self.rotate()

		elif key == keyboard.Key.left:
			self.moveLeft()

		elif key == keyboard.Key.right:
			self.moveRight()

		elif key == keyboard.Key.down:
			self.moveDown()

	# Game processing -----------------------------------------------------------------------------

	def moveDown(self):
		with self.lock:
			if self.canPlace(self.fallingFigureLocalPosition[0], self.fallingFigureLocalPosition[1]+1, self.fallingFigure):
				self.drawFallingFigure(black=True)
				self.fallingFigureLocalPosition[1] += 1
				self.drawFallingFigure()
			else:
				self.endFall()

			self.canvas.render()

	def moveLeft(self):
		with self.lock:
			if self.canPlace(self.fallingFigureLocalPosition[0]-1, self.fallingFigureLocalPosition[1], self.fallingFigure):
				self.drawFallingFigure(black=True)
				self.fallingFigureLocalPosition[0] -= 1
				self.drawFallingFigure()

				self.canvas.render()

	def moveRight(self):
		with self.lock:
			if self.canPlace(self.fallingFigureLocalPosition[0]+1, self.fallingFigureLocalPosition[1], self.fallingFigure):
				self.drawFallingFigure(black=True)
				self.fallingFigureLocalPosition[0] += 1
				self.drawFallingFigure()

				self.canvas.render()

	def rotate(self):
		with self.lock:
			rotated = self._rotateFigure({**self.fallingFigure})
			if self.canPlace(*self.fallingFigureLocalPosition, rotated):
				self.drawFallingFigure(black=True)
				self.fallingFigure = rotated
				self.drawFallingFigure()

				self.canvas.render()

	def canPlace(self, x, y, figure):
		for _x, _y in figure["data"]:
			__x, __y = x+_x, y+_y

			if __x < 0 or __x >= self.fieldSize[0] or __y < 0 or __y >= self.fieldSize[1] or (__x, __y) in self.field:
				return False

		return True

	def endFall(self):
		for coordinates in self.fallingFigure["data"]:
			self.field[self.fallingFigureLocalPosition[0]+coordinates[0], self.fallingFigureLocalPosition[1]+coordinates[1]] = self.fallingFigure["color"]

		lines = self.checkLines(self.fallingFigureLocalPosition[0], self.fallingFigure["height"])
		self.lines += lines
		if lines == 0:
			pass
		elif lines == 1:
			self.score += 100
		elif lines == 2:
			self.score += 300
		elif lines == 3:
			self.score += 700
		elif lines == 4:
			self.score += 1500

		self.level = 1 + self.lines//10
		self.interval = 0.5 / 1.1**self.level

		self.spawnFigure()

		self.drawField()		
		self.drawFallingFigure()
		self.drawNextFigure()
		self.drawScore()

	def checkLines(self, fromY, figureHeight):
		lines = 0

		#for y in range(fromY, fromY+figureHeight):
		for y in range(self.fieldSize[1]):
			full = True

			for x in range(self.fieldSize[0]):
				if not (x, y) in self.field:
					full = False
					break

			if not full:
				continue

			lines += 1

			for _y in range(y, 0, -1):
				for _x in range(self.fieldSize[0]):
					if (_x, _y-1) in self.field:
						self.field[_x, _y] = self.field[_x, _y-1]
					elif (_x, _y) in self.field:
						del self.field[_x, _y]

		return lines

	# Spawn figure --------------------------------------------------------------------------------

	def spawnFigure(self):
		if self.nextFigure == None:
			self.nextFigure = self.getRandomFigure()

		newPosition = [self.fieldSize[0]//2 - self.nextFigure["width"]//2, 0]

		if not self.canPlace(*newPosition, self.nextFigure):
			self.gameOver()
			return

		self.fallingFigureLocalPosition = newPosition
		self.fallingFigure = self.nextFigure

		self.nextFigure = self.getRandomFigure()		

	def getRandomFigure(self):
		figure = random.choice(self.figures)
		return self._rotateFigure(figure, random.randrange(1, 5))

	# Rotate --------------------------------------------------------------------------------------

	def _rotateFigure(self, figure, times=1):
		times = times % 4

		if times == 1:
			figure = self._flipX(self._swapAxes(figure))

		elif times == 2:
			figure = self._flipAxes(figure)

		elif times == 3:
			figure = self._flipY(self._swapAxes(figure))

		return figure


	def _swapAxes(self, figure):
		figure["data"] = [(y, x) for x, y in figure["data"]]
		figure["width"], figure["height"] = figure["height"], figure["width"]

		return figure

	def _flipAxes(self, figure):
		figure["data"] = [(figure["width"]-x-1, figure["height"]-y-1) for x, y in figure["data"]]

		return figure

	def _flipX(self, figure):
		figure["data"] = [(figure["width"]-x-1, y) for x, y in figure["data"]]

		return figure

	def _flipY(self, figure):
		figure["data"] = [(x, figure["height"]-y-1) for x, y in figure["data"]]

		return figure

	# Draw statics --------------------------------------------------------------------------------

	def drawInterface(self):
		self.canvas.semiPixelRectangle(1, 1, 12, 22, ComplexColors.LIGHT_WHITE)
		self.canvas.semiPixelRectangle(14, 1, 6, 6, ComplexColors.LIGHT_WHITE)

		self.canvas.print(14, 4, "Score:", ComplexColors.LIGHT_BLACK[0], ComplexColors.BLACK[1])
		self.canvas.print(14, 6, "Lines:", ComplexColors.LIGHT_BLACK[0], ComplexColors.BLACK[1])
		self.canvas.print(14, 8, "Level:", ComplexColors.LIGHT_BLACK[0], ComplexColors.BLACK[1])

	# Draw dynamics -------------------------------------------------------------------------------

	def drawField(self):
		for y in range(self.fieldSize[1]):
			for x in range(self.fieldSize[0]):
				if (x, y) in self.field:
					self.canvas.semiPixel(self.fieldPosition[0]+x, self.fieldPosition[1]+y, self.field[(x, y)])

				else:
					self.canvas.semiPixel(self.fieldPosition[0]+x, self.fieldPosition[1]+y, ComplexColors.BLACK) 

	def drawFallingFigure(self, black=False):
		if self.fallingFigure == None:
			return

		self.drawFigure(self.fieldPosition[0]+self.fallingFigureLocalPosition[0], self.fieldPosition[1]+self.fallingFigureLocalPosition[1], self.fallingFigure, black=black)

	def drawNextFigure(self):
		if self.nextFigure == None:
			return

		self.canvas.semiPixelRectangle(*self.nextFigurePosition, 4, 4, ComplexColors.BLACK, fill=True)

		(x, y) = self.nextFigurePosition

		if self.nextFigure["width"] < 3:
			x += 1

		if self.nextFigure["height"] < 3:
			y += 1

		self.drawFigure(x, y, self.nextFigure)

	def drawFigure(self, x, y, figure, black=False):
		for coordinates in figure["data"]:
			if black:
				self.canvas.semiPixel(x+coordinates[0], y+coordinates[1], ComplexColors.BLACK)
			else:
				self.canvas.semiPixel(x+coordinates[0], y+coordinates[1], figure["color"])

	def drawScore(self):
		self.canvas.print(14, 5, f"{self.score}{' '*(12-len(str(self.score)))}", ComplexColors.WHITE[0], ComplexColors.BLACK[1])
		self.canvas.print(14, 7, f"{self.lines}{' '*(12-len(str(self.lines)))}", ComplexColors.WHITE[0], ComplexColors.BLACK[1])
		self.canvas.print(14, 9, f"{self.level}{' '*(12-len(str(self.level)))}", ComplexColors.WHITE[0], ComplexColors.BLACK[1])

	# Init helpers --------------------------------------------------------------------------------

	def _loadFigures(self, *figures):
		self.figures = []

		for _figure in figures:
			_data, _color = _figure

			figure = {
				"data": [],
				"color": _color
			}

			width, height = len(_data), 0

			for x in range(len(_data)):
				if _data[x] == "█":
					height = 0b11

					figure["data"].append((x, 0))
					figure["data"].append((x, 1))

				elif _data[x] == "▀":
					height |= 0b01
					figure["data"].append((x, 0))

				elif _data[x] == "▄":
					height |= 0b10
					figure["data"].append((x, 1))

			height = 2 if height == 0b11 else 1

			figure["width"] = width
			figure["height"] = height

			self.figures.append(figure)