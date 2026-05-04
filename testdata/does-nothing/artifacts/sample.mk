GREETING := hello

.PHONY: all clean

all:
	@printf '%s\n' "$(GREETING)"

clean:
	@printf 'clean\n'
