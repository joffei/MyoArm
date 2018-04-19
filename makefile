CC		= g++
CFLAGS		= -Wall -pthread
PIOFLAGS 	= -lpigpio -lrt
MYOFLAGS	= -lmyolinux -lrt
OBJFILES	= servoReset.o
SUBOBJFILES1 	= servoCheck.o
SUBOBJFILES2 	= testCallback.o
SUBOBJFILES3	= myotest.o
TARGET		= servoReset
SUBTARGET1 	= servoCheck
SUBTARGET2 	= testCallback
SUBTARGET3	= myotest

all: $(TARGET)


$(TARGET): $(OBJFILES)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJFILES) $(LDFLAGS)

$(SUBTARGET1): $(SUBOBJFILES1)
	$(CC) $(CFLAGS) -o $(SUBTARGET1) $(SUBOBJFILES1) $(PIOFLAGS)

$(SUBTARGET2): $(SUBOBJFILES2)
	$(CC) $(CFLAGS) -o $(SUBTARGET2) $(SUBOBJFILES2) $(PIOFLAGS)

$(SUBTARGET3): $(SUBOBJFILES3)
	$(CC) $(CFLAGS) -o $(SUBTARGET3) $(SUBOBJFILES3) $(MYOFLAGS) -std=c++11

clean$(TARGET):
	rm -f $(OBJFILES) $(TARGET) *~

clean$(SUBTARGET1):
	rm -f $(SUBOBJFILES1) $(SUBTARGET1) *~

clean$(SUBTARGET2):
	rm -f $(SUBOBJFILES2) $(SUBTARGET2) *~

clean$(SUBTARGET3):
	rm -f $(SUBOBJFILES3) $(SUBTARGET3) *~

clean: clean$(TARGET) clean$(SUBTARGET1) clean$(SUBTARGET2) clean$(SUBTARGET3)

