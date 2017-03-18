Title: My Current Cpp Makefile
Date: 2014-01-04 14:51
Tags: cpp, programming
Image: 201401_My_Current_Makefile_For_Cpp/front.png
Summary: When I took my first programming course at Polytech, I used a Integrated development environment (IDE) called Visual Studio. It magically complied all my files together and formed an executable. Now a days, I've moved on from using IDEs and switch to using a text editor, Sublime Text. As the C++ code I wrote started to get more complicated and span multiple files, I needed a way to systematically complied the files together. Thus, I created a Makefile to build and organize my C++ files...

When I took my first programming course at <a href="http://engineering.nyu.edu/" target="_blank">Polytech</a>, I used an integrated development environment (IDE) called <a href="http://www.visualstudio.com/" target="_blank">Visual Studio</a>. It magically complied all my files together and formed an executable. Now a days, I've moved on from using IDEs and switch to using a text editor, <a href="http://www.sublimetext.com/" target="_blank">Sublime Text</a>.[^sublimetext] As the C++ code I wrote started to get more complicated and span multiple files, I needed a way to systematically complied the files together. Thus, I created a Makefile to build and organize my C++ files.

## Makefile Logic

```makefile
CXX = g++
CXXFLAGS=-g -O2 -Wall -Wconversion
```

The first two lines of my Makefile defines the complier and its flags. I especially like the `-Wconversion` flag, since I prefer code that have explicit type conversions. This flag issues a warning when a type conversion is implicit.[^diff]

```makefile
SOURCES=$(wildcard src/**/*.cpp src/*.cpp)
OBJECTS=$(patsubst src/%.cpp,bin/%.o,$(SOURCES))
```

The `wildcard` function uses a pattern to find the sources for compilation. In this case, all the filenames in src folder and its subfolders are stored into `SOURCES`. The `patsubst` function changes the extension of `SOURCES` to `.o` extension and defines a destination folder, `bin`, for the complied objects.

```makefile
EXECUT=build/test.exe
MAIN=src/main.cpp
```

This defines the location of the `main()` function and the output executable. I have gotten into the habit of creating an executable for quick testing and having a single file, `main.cpp`, defining the main function of my program.

```makefile
LIB_SOURCES=$(filter-out $(MAIN), $(SOURCES))
LIB_OBJ=$(patsubst src/%.cpp,bin/%.o,$(LIB_SOURCES))
LIB_TARGET=build/libYOURLIBRARY.a
SO_TARGET=$(patsubst %.a,%.so,$(LIB_TARGET))
```

If you wanted to build libraries, these variables give the sources and destination for the libraries. `filter-out` removes the main.cpp from the library compilation. There are two types of libraries, static and dynamic. The former uses a `.a` extension while the latter uses a `.so` extension.

## Makefile Usage

With all the variables defined, the Makefile is used to do various actions. My most used action is the to build an executable from all the source files:

```makefile
exec: build $(OBJECTS)
    $(CXX) $(CXXFLAGS) -o $(EXECUT) $(OBJECTS)
    @./$(EXECUT)
```

This code is called by running `make exec` in the same directory as the Makefile.[^makefile] The components `build` and `$(OBJECTS)` on the same line of `exec` must run or compile before the body can be executed. The body of `exec` compiles the executable and then runs it. On the last line, `@` is used to issue a command on the shell.

```makefile
build:
    @mkdir -p build
    @mkdir -p bin
```

The first component of `exec`, `build`, simply makes two directories, build and bin. The second component, `$(OBJECTS)`, is syntactic sugar to reference the variable, `OBJECTS`. The make utility knows to take these files and compile them when it is a component to an action. In this case, it is a component to `exec`. If `OBJECTS` were not redefined to be in the new folder, bin, the make utility would compile the `.cpp` files into the same location as the source files, doubling the number of files in the src folder. [^pycache] Since the `OBJECTS` were given a new home in bin, the following is needed:

```makefile
bin/%.o: src/%.cpp
    $(CXX) -c $(CXXFLAGS) -o $@ $<
```

This tells the make utility to compile all the `.cpp` files into the bin folder. There is some more syntactic sugar here: `$@` refers to the action name, `bin/%.o` and `$<` refers to component, `src/%.cpp`.

```makefile
clean:
    rm -rf build bin $(OBJECTS)
```

The clean action removes all the output files created by the Makefile. This gives you a clean slate, with only the source code. You can run this action with `make clean`.

The rest of my Makefile defines actions for building static and dynamic libraries. I put the `exec` action first, which makes it the default action. In other words, I can just run `make` to run `make exec`. It is quite exhilarating using Makefile for compilation rather than an IDE.

## The Makefile in its Entirety

```{makefile}
CXX = g++
CXXFLAGS=-g -O2 -Wall -Wconversion

SOURCES=$(wildcard src/**/*.cpp src/*.cpp)
OBJECTS=$(patsubst src/%.cpp,bin/%.o,$(SOURCES))

EXECUT=build/test.exe
MAIN=src/main.cpp

LIB_SOURCES=$(filter-out $(MAIN), $(SOURCES))
LIB_OBJ=$(patsubst src/%.cpp,bin/%.o,$(LIB_SOURCES))
LIB_TARGET=build/libYOURLIBRARY.a
SO_TARGET=$(patsubst %.a,%.so,$(LIB_TARGET))

exec: build $(OBJECTS)
    $(CXX) $(CXXFLAGS) -o $(EXECUT) $(OBJECTS)
    @./$(EXECUT)

all: build $(OBJECTS) lib dyn exec

libexec: build $(OBJECTS) lib
    $(CXX) $(CXXFLAGS) -o $(EXECUT) $(MAIN) $(LIB_TARGET)

test:
    gdb $(EXECUT)

bin/%.o: src/%.cpp
    $(CXX) -c $(CXXFLAGS) -o $@ $<

run:
    @./$(EXECUT)

lib: build $(LIB_OBJ)
    ar rcs $(LIB_TARGET) $(LIB_OBJ)
    ranlib $(LIB_TARGET)

dyn: build $(LIB_OBJ)
    $(CXX) -shared -o $(SO_TARGET) $(LIB_OBJ)

build:
    @mkdir -p build
    @mkdir -p bin

clean:
    rm -rf build bin $(OBJECTS)
```

[^sublimetext]: I recently switched over to Sublime Text 3 and it is AMAZING.

[^diff]: The word, implicit, always reminds me of calculus.

[^makefile]: This is because the make utility looks in the current directory for the makefile, otherwise you can use the flag -f to give the Makefile.

[^pycache]: Python 2 use to do this with its .pyc files, but in Python 3, it puts the complied files into a pycache directory. Very awesome.
