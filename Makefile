all:
	g++ src/main.cpp -o main -lboost_system -lboost_filesystem

clean: 
	rm main src/*.gch
