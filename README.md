API for Noisebridge
===================

This is a very simple Python WSGI App that provides what should hopefully be a stable API for fun things in the Noisebridge space.

Using the API
-------------

The API is currently only available within the space. Once we have
authorisation running, this will change.

The API is RESTful, and can be called at the URL:

http://api.noisebridge.net/[call]

For instance, to open the door using curl:

```bash
    curl -X POST http://api.noisebridge.net/gate/open
```

### GET /hello/[name]

Returns 'hello [name]'

### POST /gate/open

Opens the door. Returns a JSON dictionary:

```json
    {
    success: boolean,
    message: string
    }
```

Where success is true if the door was buzzed open.

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

You'll need sudo powers on pony. Check out the code using git:

```bash
    git clone /var/local/noise_api/
```

Make your changes, and test them locally using 

```bash
    python api.py --debug
```

When you're ready to deploy, commit the code, then pull it out to the runningversion of api.py.

```bash
    cd /var/local/noise_api/
    sudo git pull [your cloned directory goes here]
    sudo /etc/init.d/apache2 restart
```
