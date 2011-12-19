.PHONY: install all

all:

install: apache2-conf
	install -C --mode=0755 --owner=root --group=root ./apache2-conf /etc/apache2/sites-available/noisebridge-api
	apache2ctl restart
