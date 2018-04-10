CC		= g++
CFLAGS		= -Wall -pthread
LDFLAGS 	= -lpigpio -lrt
OBJFILES	= servoReset.o
SUBOBJFILES1 	= servoCheck.o
SUBOBJFILES2 	= testCallback.o
TARGET		= servoReset
SUBTARGET1 	= servoCheck
SUBTARGET2 	= testCallback

all: $(TARGET)


$(TARGET): $(OBJFILES)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJFILES) $(LDFLAGS)

$(SUBTARGET1): $(SUBOBJFILES1)
	$(CC) $(CFLAGS) -o $(SUBTARGET1) $(SUBOBJFILES1) $(LDFLAGS)

$(SUBTARGET2): $(SUBOBJFILES2)
	$(CC) $(CFLAGS) -o $(SUBTARGET2) $(SUBOBJFILES2) $(LDFLAGS)

clean$(TARGET):
	rm -f $(OBJFILES) $(TARGET) *~

clean$(SUBTARGET1):
	rm -f $(SUBOBJFILES1) $(SUBTARGET1) *~

clean$(SUBTARGET2):
	rm -f $(SUBOBJFILES2) $(SUBTARGET2) *~
	
clean: clean$(TARGET) clean$(SUBTARGET1) clean$(SUBTARGET2)

