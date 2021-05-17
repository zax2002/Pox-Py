from modules.canvas.canvasBase import CanvasBase
from modules.canvas.complexColors import ComplexColors

class Canvas(CanvasBase):
	def charRectangle(self, x, y, width, height, char, foreColor=None, backColor=None, fill=False):
		xTo = x+width-1
		yTo = y+height-1

		if x < 0 or x >= self.width or y < 0 or y >= self.height or xTo < 0 or xTo >= self.width or yTo < 0 or yTo >= self.height:
			return

		if foreColor == None:
			foreColor = self.currentForeColor
		else:
			self.currentForeColor = foreColor

		if backColor == None:
			backColor = self.currentBackColor
		else:
			self.currentBackColor = backColor

		if fill:
			for _y in range(y, yTo+1):
				for _x in range(x, xTo+1):
					self.char(_x, _y, char, foreColor, backColor, False)

		else:
			for _x in range(x, xTo+1):
				self.char(_x, y, char, foreColor, backColor, False)
				self.char(_x, yTo, char, foreColor, backColor, False)

			for _y in range(y+1, yTo):
				self.char(x, _y, char, foreColor, backColor, False)
				self.char(xTo, _y, char, foreColor, backColor, False)
			
	def semiPixelRectangle(self, x, semiY, width, semiHeight, complexColor=None, fill=False):
		y = semiY//2
		xTo = x+width-1
		yTo = y+(semiHeight+1)//2
		semiYTo = semiY+semiHeight-1

		if x < 0 or x >= self.width or y < 0 or y >= self.height or xTo < 0 or xTo >= self.width or yTo < 0 or yTo >= self.height:
			return

		if complexColor == None:
			complexColor = ComplexColors.fromForeColor(self.currentForeColor)
		else:
			self.currentForeColor = complexColor[0]

		if fill:
			for _semiY in range(semiY, semiYTo+1):
				for _x in range(x, xTo+1):
					self.semiPixel(_x, _semiY, complexColor, False)

		else:
			for _x in range(x, xTo+1):
				self.semiPixel(_x, semiY, complexColor, False)
				self.semiPixel(_x, semiYTo, complexColor, False)

			for _semiY in range(semiY+1, semiYTo):
				self.semiPixel(x, _semiY, complexColor, False)
				self.semiPixel(xTo, _semiY, complexColor, False)

	def print(self, x, y, text, foreColor=None, backColor=None):
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

		text = text.replace("\\n", "\\\\n")

		i = 0
		for _x in range(x, x+len(text)):
			if _x >= self.width:
				return

			self.char(_x, y, text[i], foreColor, backColor, False)
			i += 1