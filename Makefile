.PHONY: all install enable clean package

all:

install: apache2-conf
	install -C --mode=0755 --owner=root --group=root ./apache2-conf $(DESTDIR)/etc/apache2/sites-available/noisebridge-api

clean:

enable:
	a2ensite noisebridge-api
	a2enmod wsgi
	apache2ctl restart

package:
	dpkg-buildpackage -rfakeroot
