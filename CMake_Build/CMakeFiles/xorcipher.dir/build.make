# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build"

# Include any dependencies generated for this target.
include CMakeFiles/xorcipher.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/xorcipher.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/xorcipher.dir/flags.make

CMakeFiles/xorcipher.dir/cipher.cpp.o: CMakeFiles/xorcipher.dir/flags.make
CMakeFiles/xorcipher.dir/cipher.cpp.o: cipher.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/xorcipher.dir/cipher.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/xorcipher.dir/cipher.cpp.o -c "/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build/cipher.cpp"

CMakeFiles/xorcipher.dir/cipher.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/xorcipher.dir/cipher.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build/cipher.cpp" > CMakeFiles/xorcipher.dir/cipher.cpp.i

CMakeFiles/xorcipher.dir/cipher.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/xorcipher.dir/cipher.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build/cipher.cpp" -o CMakeFiles/xorcipher.dir/cipher.cpp.s

# Object files for target xorcipher
xorcipher_OBJECTS = \
"CMakeFiles/xorcipher.dir/cipher.cpp.o"

# External object files for target xorcipher
xorcipher_EXTERNAL_OBJECTS =

libxorcipher.so: CMakeFiles/xorcipher.dir/cipher.cpp.o
libxorcipher.so: CMakeFiles/xorcipher.dir/build.make
libxorcipher.so: CMakeFiles/xorcipher.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library libxorcipher.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/xorcipher.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/xorcipher.dir/build: libxorcipher.so

.PHONY : CMakeFiles/xorcipher.dir/build

CMakeFiles/xorcipher.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/xorcipher.dir/cmake_clean.cmake
.PHONY : CMakeFiles/xorcipher.dir/clean

CMakeFiles/xorcipher.dir/depend:
	cd "/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build" "/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build" "/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build" "/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build" "/mnt/c/Users/steph/Desktop/School/Programming/Exercise 3/XORCipher/CMake_Build/CMakeFiles/xorcipher.dir/DependInfo.cmake" --color=$(COLOR)
.PHONY : CMakeFiles/xorcipher.dir/depend

