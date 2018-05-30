## Install dependencies

### Use `virtualenv`

We work in a [virtualenv](https://virtualenv.pypa.io/en/stable/) called `bgp` and highly recommend you to do the same.
Have a look at [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html) for the easiest way to start.

```
mkvirtualenv -p /usr/local/bin/python3 bgp
```

From now on you can use `workon bgp` to be in the virtual environment.

### Download dependencies

```
cd
mkdir git
cd git
```

clone all needed repositories

```
git clone git@github.com:CAIDA/bgpstream.git bgpstream
git clone git@github.com:rtrlib/rtrlib.git rtrlib
git clone git@github.com:rtrlib/python-binding.git pyrtrlib
```


### Build dependencies

#### bgpstream

```
cd ~/git/bgpstream
./configure
make
make install
```

#### rtrlib

```
cd ~/git/rtrlib
cmake -Wno-dev -D CMAKE_BUILD_TYPE=Release .
make
make install
```

```
workon bgp
cd ~/git/pyrtrlib
python setup.py build
python setup.py install
```

### install remaining dependencies via `pip`

```
workon bgp
pip install -r BGPDisplay/requirements.txt
```

# bgp-group


- rrc00
- rrc03

Vantage Punkte untersuchen

- wieviele
- valid/invalid
- welche präfixe



## Ripe Dump - Zeiten

### rrc00, rrc03

- 00:00
- 08:00
- 16:00

## Route views - Zeiten

###

- 00:00
- 02:00
- 04:00
- 06:00
- 08:00
- ...

## Vantage Points vs Route Collectoren

Vantage Point hat ASN & IP
