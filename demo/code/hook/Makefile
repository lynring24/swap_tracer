LIB=./hook.so
LIBS=-ldl 
LDFLAGS="-Wl,--no-as-needed"

CC=g++


compile: hook.cpp 
	$(CC) -I.  -o $(LIB) -shared -fPIC  -ldl -lunwind

run: compile
	@LD_PRELOAD=./$(LIB) $(TEST_DIR)/$(RUN_ARG)

clean:
	@rm -rf $(LIB) *.o

