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
    sudo make install
```
