auth: auth.o
	g++ -o auth -fsanitize=address auth.o

auth.o: auth.cpp
	g++ -c auth.cpp

clean:
	rm auth.o auth