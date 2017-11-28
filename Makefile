test:
	py.test -v tests
push-update:
	git add .
	git ci -m "`date`"
	git ps
clear-useless:
	python clear_useless.py
