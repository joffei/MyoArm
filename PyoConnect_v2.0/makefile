CC		= python
ROOT		= sudo
DAEMON		= pigpiod
TARGET		= PyoManager
SUBTARGET1	= baseUnit
SUBTARGET2	= lowerArmUnit
SPATH		= scripts/
EXT1		= .pyc
EXT2		= .py

all: daemon $(TARGET)

daemon:
	$(ROOT) $(DAEMON)

$(TARGET):
	$(CC) $(TARGET)$(EXT1)

$(SUBTARGET1):
	$(CC) $(SPATH)$(SUBTARGET1)$(EXT2)

$(SUBTARGET2):
	$(CC) $(SPATH)$(SUBTARGET2)$(EXT2)
