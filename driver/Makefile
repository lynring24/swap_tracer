CC=g++
LIBS="/usr/lib/libfl.a"


all: brew libhmalloc.a

brew: lex.yy.c 
	$(CC) -o brew -std=c++11 lex.yy.c -I$(LIBS)

lex.yy.c: brew.l
	flex brew.l
libhmalloc.a: hmalloc.o
	ar -rf libhmalloc.a hmalloc.o
hmalloc.o:
	gcc -c -o hmalloc.o hmalloc.c
clean:
	rm  brew libhmalloc.a 
