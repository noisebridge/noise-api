API for Noisebridge
===================

This is a very simple Python WSGI App that provides a RESTful API for fun things in the Noisebridge space.

In the Noisebridge tradition, it's not stable! It will, however try to break in
as noisy a way as possible if things change.

Using the API
-------------

The API is currently only available within the space. Once we have
authorisation running, this will change.

The API is RESTful, and can be called at the URL:

http://api.noisebridge.net/[call]

For instance, to open the door using curl:

```bash
    curl -X POST -d open=True http://api.noisebridge.net/gate/
```

### GET /hello/[name]

Returns 'hello [name]'

### GET /spaceapi/

Returns Noisebridge status, formatted as per http://hackerspaces.nl/spaceapi/

### GET /gate/

Gets interesting stats about the gate. Currently:

```json
    {
    ringing: boolean
    }
```

Where 'ringing' is true if the gate buzzer is ringing at that moment, or in the
last few seconds, as users may push the button for a very short time. The
amount of time that this state is cached is totally up to the Gateman daemon
that runs to interact with the gate hardware.

### POST /gate/ 

With open=True, opens the door. Returns a 300 error if unsuccessful, and
the following additions to the /gate/ stats if successful:

```json
    {
    open : True
    message: string
    }
```

With key=XXXX, will optionally check the key against the door code list. 

Note that this isn't a required field. Currently if you omit the key field, the
door will always open. It's intended to optionally allow other apps to offer
the same door code authentication that we use for the phone booth entry. 

### POST /gate/key/[doorcode]

With create=True and an existing, valid doorcode, redirects to a URL of the form
/gate/key/[newdoorcode] which gives a valid new doorcode to open the door.

With preferred=[number] you can suggest a doorcode you'd like to use. It's not
guaranteed that the preferred option will be returned.

Suppose you have a doorcode 8499146, and you'd like to give a friend a new doorcode. She asks if she can have the number '7895473'

```bash
curl -v -X POST -d create=True -d preferred=7895473 http://localhost:8080/gate/key/8499146
```

would return something like this:
```
> POST /gate/key/8499146 HTTP/1.1
> User-Agent: curl/7.26.0
> Host: localhost:8080
> Accept: */*
> Content-Length: 29
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 29 out of 29 bytes
* additional stuff not fine transfer.c:1037: 0 0
* HTTP 1.0, assume close after body
< HTTP/1.0 303 See Other
< Date: Mon, 05 Nov 2012 05:07:29 GMT
< localhost - - [04/Nov/2012 21:07:29] "POST /gate/key/8499146 HTTP/1.1" 303 0
Server: WSGIServer/0.1 Python/2.7.3rc2
< Content-Length: 0
< Content-Type: text/html; charset=UTF-8
< Location: http://localhost:8080/gate/key/7895473
< 
* Closing connection #0
```

The Location header contains the new doorcode.


### POST /audio/

With say=[TEXT] will convert the TEXT into speech, and announce it to the space.

Adding to the API
-----------------

api.py is a [Bottle](http://bottlepy.org/docs/dev/). It should be pretty self
explanatory, even if you don't know much Python.

Just add a function of the form:

```python
@api_app.route("/myurl/")
def myfunc()
    do_something_in_the_space()
    return { 'success' : True, 'OMG IT WORXORRED' }
```

Deploying your new API
----------------------

You'll need sudo powers on minotaur. Check out the code using git:

```bash
    git clone git@github.com:noisebridge/noise-api.git
```

Make your changes, and test them locally using 

```bash
   python api.py --debug
```

When you're ready to deploy, change the Debian changelog in debian/changelog
(the [git-dch](http://honk.sigxcpu.org/projects/git-buildpackage/manual-html/gbp.man.git.dch.html)
program can help with this), and commit the code to the github repository..

Log onto minotaur, clone the git repository, and make a Debian package. Install it using dpkg -i

```bash
   git clone git://github.com/noisebridge/noise-api.git
   cd noise-api
   make package
   sudo dpkg -i ../noisebridge-api_0[whatever the version number is]*.deb

```
