#!/bin/bash
SRCDIR = $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
VPATH  = $(SRCDIR)

## Generate the list of files.
FILES  = $(shell ls ${SRCDIR} | grep '\.py')
FILES += README.md
FILES += LICENSE
FILES += animations

## Generate the tarball
TARBALL=dcfurs-badge-dc27.tar.gz
$(TARBALL): $(FILES)
	tar -czf $@ -C ${SRCDIR} ${FILES}

clean:
	rm -f $(TARBALL)

