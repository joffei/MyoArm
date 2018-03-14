CC	= g++
CFLAGS	= -Wall -pthread
LDFLAGS = -lpigpio -lrt
OBJFILES= servoReset.o
TARGET	= servoReset


all: $(TARGET)


$(TARGET): $(OBJFILES)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJFILES) $(LDFLAGS)

clean:
	rm -f $(OBJFILES) $(TARGET) *~
