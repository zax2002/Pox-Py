from colorama import Fore as ForeColors
from colorama import Back as BackColors

class ComplexColors:
	RESET 		  = ( ForeColors.RESET, 		  BackColors.RESET			 )

	LIGHT_BLACK   = ( ForeColors.LIGHTBLACK_EX,   BackColors.LIGHTBLACK_EX	 )
	LIGHT_RED 	  = ( ForeColors.LIGHTRED_EX, 	  BackColors.LIGHTRED_EX	 )
	LIGHT_GREEN   = ( ForeColors.LIGHTGREEN_EX,   BackColors.LIGHTGREEN_EX	 )
	LIGHT_YELLOW  = ( ForeColors.LIGHTYELLOW_EX,  BackColors.LIGHTYELLOW_EX	 )
	LIGHT_BLUE 	  = ( ForeColors.LIGHTBLUE_EX, 	  BackColors.LIGHTBLUE_EX	 )
	LIGHT_MAGENTA = ( ForeColors.LIGHTMAGENTA_EX, BackColors.LIGHTMAGENTA_EX )
	LIGHT_CYAN 	  = ( ForeColors.LIGHTCYAN_EX, 	  BackColors.LIGHTCYAN_EX	 )
	LIGHT_WHITE   = ( ForeColors.LIGHTWHITE_EX,	  BackColors.LIGHTWHITE_EX	 )

	BLACK 		  = ( ForeColors.BLACK, 		  BackColors.BLACK			 )
	RED 		  = ( ForeColors.RED, 			  BackColors.RED			 )
	GREEN 		  = ( ForeColors.GREEN, 		  BackColors.GREEN			 )
	YELLOW 		  = ( ForeColors.YELLOW, 		  BackColors.YELLOW			 )
	BLUE 		  = ( ForeColors.BLUE, 			  BackColors.BLUE			 )
	MAGENTA 	  = ( ForeColors.MAGENTA, 		  BackColors.MAGENTA		 )
	CYAN 		  = ( ForeColors.CYAN, 			  BackColors.CYAN			 )
	WHITE 		  = ( ForeColors.WHITE, 		  BackColors.WHITE			 )

	_fromForeColor = {
		ForeColors.RESET: 			RESET,

		ForeColors.LIGHTBLACK_EX: 	LIGHT_BLACK,
		ForeColors.LIGHTRED_EX: 	LIGHT_RED,
		ForeColors.LIGHTGREEN_EX: 	LIGHT_GREEN,
		ForeColors.LIGHTYELLOW_EX: 	LIGHT_YELLOW,
		ForeColors.LIGHTBLUE_EX: 	LIGHT_BLUE,
		ForeColors.LIGHTMAGENTA_EX: LIGHT_MAGENTA,
		ForeColors.LIGHTCYAN_EX: 	LIGHT_CYAN,
		ForeColors.LIGHTWHITE_EX: 	LIGHT_WHITE,

		ForeColors.BLACK: 			BLACK,
		ForeColors.RED: 			RED,
		ForeColors.GREEN: 			GREEN,
		ForeColors.YELLOW: 			YELLOW,
		ForeColors.BLUE: 			BLUE,
		ForeColors.MAGENTA: 		MAGENTA,
		ForeColors.CYAN: 			CYAN,
		ForeColors.WHITE: 			WHITE
	}

	_fromBackColor = {
		BackColors.RESET: 			RESET,

		BackColors.LIGHTBLACK_EX: 	LIGHT_BLACK,
		BackColors.LIGHTRED_EX: 	LIGHT_RED,
		BackColors.LIGHTGREEN_EX: 	LIGHT_GREEN,
		BackColors.LIGHTYELLOW_EX: 	LIGHT_YELLOW,
		BackColors.LIGHTBLUE_EX: 	LIGHT_BLUE,
		BackColors.LIGHTMAGENTA_EX: LIGHT_MAGENTA,
		BackColors.LIGHTCYAN_EX: 	LIGHT_CYAN,
		BackColors.LIGHTWHITE_EX: 	LIGHT_WHITE,

		BackColors.BLACK: 			BLACK,
		BackColors.RED: 			RED,
		BackColors.GREEN: 			GREEN,
		BackColors.YELLOW: 			YELLOW,
		BackColors.BLUE: 			BLUE,
		BackColors.MAGENTA: 		MAGENTA,
		BackColors.CYAN: 			CYAN,
		BackColors.WHITE: 			WHITE
	}

	@classmethod
	def fromForeColor(cls, foreColor):
		return cls._fromForeColor[foreColor]

	@classmethod
	def fromBackColor(cls, backColor):
		return cls._fromBackColor[backColor]