CC=g++
LIBS="/usr/lib/libfl.a"


all: tint mlock

tint: tint.yy.c 
	$(CC) -o tint -std=c++11 tint.yy.c -I$(LIBS)

tint.yy.c: tint.l
	flex -o tint.yy.c tint.l

mlock: mlock.yy.c 
	$(CC) -o mlock -std=c++11 mlock.yy.c -I$(LIBS)

mlock.yy.c: mlock.l
	flex -o mlock.yy.c mlock.l

clean:
	rm  tint mlock 
