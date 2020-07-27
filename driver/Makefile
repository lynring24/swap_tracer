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
hmalloc.so:
	gcc -fPIC -shared -o hmalloc.so hmalloc.c -Wl,--no-as-needed -ldl
clean:
	rm  brew libhmalloc.a 
