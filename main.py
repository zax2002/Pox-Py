from modules.canvas.canvas import Canvas
from modules.canvas.complexColors import ComplexColors
from modules.tetris.tetris import Tetris

import time

# canvas = Canvas(100, 50)
# canvas.init()

#canvas.char(2, 1, "X")
#canvas.charRectangle(2, 1, 6, 3, "X")

# canvas.semiPixelRectangle(2, 2, 20, 20, ComplexColors.LIGHTBLUE)
# canvas.render()

# for y in range(20):
# 	for x in range(20):
# 		if (y) % 2:
# 			canvas.semiPixel(x, y, ComplexColors.LIGHTRED)
# 		else:
# 			canvas.semiPixel(x, y, ComplexColors.RED)

# canvas.render()

# canvas.clear()

# canvas.semiPixelRectangle(2, 2, 66, 34, ComplexColors.LIGHTWHITE)

# canvas.semiPixelRectangle(4, 4, 3, 3, ComplexColors.LIGHTRED, fill=True)

# canvas.semiPixelRectangle(4, 9, 3, 3, ComplexColors.LIGHTRED, fill=True)
# canvas.semiPixelRectangle(7, 9, 3, 3, ComplexColors.RED, fill=True)

# canvas.semiPixelRectangle(4, 15, 3, 3, ComplexColors.LIGHTRED)

# canvas.semiPixelRectangle(4, 20, 3, 3, ComplexColors.LIGHTRED)
# canvas.semiPixelRectangle(6, 19, 3, 1, ComplexColors.RED)
# canvas.semiPixelRectangle(7, 21, 4, 1, ComplexColors.RED)
# canvas.semiPixelRectangle(6, 23, 2, 1, ComplexColors.RED)

# canvas.semiPixel(5, 26, ComplexColors.LIGHTRED)
# canvas.semiPixel(4, 27, ComplexColors.LIGHTRED)
# canvas.semiPixel(6, 27, ComplexColors.LIGHTRED)
# canvas.semiPixel(5, 28, ComplexColors.LIGHTRED)

# canvas.semiPixel(5, 31, ComplexColors.LIGHTRED)
# canvas.semiPixel(4, 32, ComplexColors.LIGHTRED)
# canvas.semiPixel(6, 32, ComplexColors.LIGHTRED)
# canvas.semiPixel(5, 33, ComplexColors.LIGHTRED)


# canvas.semiPixelRectangle(63, 4, 3, 3, ComplexColors.LIGHTBLUE, fill=True)
# canvas.semiPixelRectangle(62, 4, 1, 3, ComplexColors.BLUE, fill=True)

# canvas.render()


# colors = [*ComplexColors._fromForeColor.values()]
# for y in range(100):
# 	for x in range(100):
# 		color = colors[((x+y*100)%16)+1]
# 		canvas.semiPixel(x, y, color)

# canvas.render()

# input()
# canvas.char(0, 0, "", ComplexColors.RESET[0], ComplexColors.RESET[1])
# canvas.render()


tetris = Tetris()

# input()
# tetris.canvas.char(0, 0, "", ComplexColors.RESET[0], ComplexColors.RESET[1])
# tetris.canvas.render()