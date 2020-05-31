.PHONY : test check build clean push_release

test:
	nosetests --verbose --with-coverage --cover-package bcltools

check:
	flake8 bcltools && echo OK
	yapf -r --diff bcltools && echo OK

build:
	python setup.py sdist bdist_wheel

clean:
	rm -rf build
	rm -rf dist
	rm -rf bcltools.egg-info
	rm -rf docs/_build
	rm -rf docs/api

bump_patch:
	bumpversion patch

bump_minor:
	bumpversion minor

bump_major:
	bumpversion major

push_release:
	git push && git push --tags