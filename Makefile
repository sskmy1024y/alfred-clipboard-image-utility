VENV=venv

all :
	@echo "Run \`make workflow\` to create the Alfred workflow file after removing the old one if it exists."

distclean :
	rm -f ./alfred-clipboard-image-utility.alfredworkflow

clean :
	rm -f alfred.py
	rm -rf ${VENV}
	find . -iname "*.pyc" -delete

install : 
	pip install -r requirements.txt --upgrade --force-reinstall

lib :
	cp `python sitepackages.py`/alfred.py alfred.py

dev : install \
	lib

zip :
	zip -r ./alfred-clipboard-image-utility.alfredworkflow . -x "*.git*" "*venv*" .DS_Store .gitignore Makefile requirements.txt README.md sitepackages.py

workflow : distclean \
	install \
	lib \
	zip
