CC=g++
LIBS="/usr/lib/libfl.a"
brew: lex.yy.c 
	$(CC) -o brew -std=c++11 lex.yy.c -I$(LIBS)

lex.yy.c: brew.l
	flex brew.l

clean:
	rm  brew 
