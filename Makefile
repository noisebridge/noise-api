.PHONY: all install enable clean package

all:

install: apache2-conf api.py
	mkdir -p $(DESTDIR)/usr/lib/noisebridge-api
	mkdir -p $(DESTDIR)/etc/apache2/sites-available
	install -C --mode=0644 --owner=root --group=root api.py $(DESTDIR)/usr/lib/noisebridge-api
	install -C --mode=0644 --owner=root --group=root api.wsgi $(DESTDIR)/usr/lib/noisebridge-api
	install -C --mode=0644 --owner=root --group=root bottle.py $(DESTDIR)/usr/lib/noisebridge-api
	install -C --mode=0644 --owner=root --group=root mimeparse.py $(DESTDIR)/usr/lib/noisebridge-api
	install -C --mode=0644 --owner=root --group=root gate.tpl $(DESTDIR)/usr/lib/noisebridge-api
	install -C --mode=0755 --owner=root --group=root apache2-conf $(DESTDIR)/etc/apache2/sites-available/noisebridge-api

clean:

enable:
	a2ensite noisebridge-api
	a2enmod wsgi
	apache2ctl restart

package:
	dpkg-buildpackage -rfakeroot
