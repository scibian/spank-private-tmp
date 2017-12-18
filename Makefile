LIBDIR  ?= /usr/lib
CONFDIR ?= /etc/slurm-llnl/plugstack.conf.d

all: private-tmp.so

private-tmp.so: hpc2n-tmpdir.c
	gcc -std=gnu99 -Wall -o private-tmp.o -fPIC -c hpc2n-tmpdir.c
	gcc -shared -o private-tmp.so private-tmp.o

install:
	mkdir -p $(DESTDIR)/$(LIBDIR)/slurm
	mkdir -p $(DESTDIR)/$(CONFDIR)
	install -m 755 private-tmp.so $(DESTDIR)/$(LIBDIR)/slurm/
	install -m 644 private-tmp.conf $(DESTDIR)/$(CONFDIR)

clean:
	rm -f private-tmp.o private-tmp.so
