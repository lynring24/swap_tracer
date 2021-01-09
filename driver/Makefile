CC=g++
LIBS="/usr/lib/libfl.a"


all: brew 

brew: brew.yy.c 
	$(CC) -o brew -std=c++11 brew.yy.c -I$(LIBS)

brew.yy.c: brew.l
	flex -o brew.yy.c brew.l


clean:
	rm  brew  
