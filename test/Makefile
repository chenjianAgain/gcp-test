GIT_HASH := $(shell git log -n 1 --pretty=format:"%H")
EDIT_WORKSPACE := $(shell git diff --shortstat | grep -q changed && echo 1)
EDIT_INDEX := $(shell git diff --cached --shortstat | grep -q changed && echo 1)
GIT_BRANCH := $(shell git branch --contains $(GIT_HASH) | egrep '^\*' | sed -r 's/\* //g')
GIT_BRANCH_IS_DETACHED_PATT := '(\(no branch\)|\(detached )'
GIT_BRANCH_IS_DETACHED := $(shell echo "$(GIT_BRANCH)" | egrep -q $(GIT_BRANCH_IS_DETACHED_PATT) && echo 1)
VERSION := 0
ifeq "$(GIT_BRANCH_IS_DETACHED)" "1"
	VERSION := $(shell git tag --points-at $(GIT_HASH) | head -1)
else
	$(error no version to make, please check out target tag)
endif

.PHONY: rpm
rpm: clean
	PYVER=3.6 MODULE_VERSION=$(VERSION) python3.6 setup.py bdist_rpm --python python3.6 --binary-only
	mkdir -p dist/RPMS/noarch
	cp dist/*noarch* dist/RPMS/noarch/

test:
	nosetests

clean:
	rm -rf dist/

install:
	MODULE_VERSION=$(VERSION) python setup.py install
