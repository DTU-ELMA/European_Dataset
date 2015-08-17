
windloop_cosmo.so: windloop_cosmo.o
#	gcc -Wall -lm -shared -Wl,-install_name,windloop_cosmo.so -o windloop_cosmo.so windloop_cosmo.o
	gcc -Wall -lm -shared -Wl,-soname,windloop_cosmo.so -o windloop_cosmo.so windloop_cosmo.o

windloop_cosmo.o:	windloop_cosmo.c
	gcc -Wall -lm -c -fPIC -O3 windloop_cosmo.c -o windloop_cosmo.o

