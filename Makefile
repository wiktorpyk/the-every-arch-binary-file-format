CC = gcc
CFLAGS = -fPIC -Wall -Wextra
LDFLAGS = -shared
TARGET_LIB = libhello.so
TARGET_BIN = main

ARCHS = x86_64 arm riscv64

all: $(addprefix build/, $(ARCHS)) combine

build/x86_64: main.c build/x86_64/$(TARGET_LIB)
	mkdir -p build/x86_64
	$(CC) -o build/x86_64/$(TARGET_BIN) $< -Lbuild/x86_64 -lhello -Wl,-rpath=.

build/x86_64/$(TARGET_LIB): hello.c
	mkdir -p build/x86_64
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

build/arm: main.c build/arm/$(TARGET_LIB)
	mkdir -p build/arm
	aarch64-linux-gnu-gcc -o build/arm/$(TARGET_BIN) $< -Lbuild/arm -lhello -Wl,-rpath=.

build/arm/$(TARGET_LIB): hello.c
	mkdir -p build/arm
	aarch64-linux-gnu-gcc $(CFLAGS) $(LDFLAGS) -o $@ $^

build/riscv64: main.c build/riscv64/$(TARGET_LIB)
	mkdir -p build/riscv64
	riscv64-linux-gnu-gcc -o build/riscv64/$(TARGET_BIN) $< -Lbuild/riscv64 -lhello -Wl,-rpath=.

build/riscv64/$(TARGET_LIB): hello.c
	mkdir -p build/riscv64
	riscv64-linux-gnu-gcc $(CFLAGS) $(LDFLAGS) -o $@ $^

combine: all
	python3 combine.py

clean:
	rm -rf build build_combined temp