
windloop.so: windloop.o
	gcc -Wall -lm -shared -Wl,-soname,windloop.so -o windloop.so windloop.o

windloop.o:	windloop.c
	gcc -Wall -lm -c -fPIC -O3 windloop.c -o windloop.o

windloop2.so: windloop2.o
	gcc -Wall -lm -shared -Wl,-soname,windloop2.so -o windloop2.so windloop2.o

windloop2.o:	windloop2.c
	gcc -Wall -lm -c -fPIC -O3 windloop2.c -o windloop2.o

