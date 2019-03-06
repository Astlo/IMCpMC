# MCpMC
Statistical model checking of pMC

This prototype is implemented using python 3.6 (we give no guaranties for other versions)

Dependencies:
  - sympy : to represent expressions (to install: sudo pip install sympy)
  - ply : to parse the models (to install: pip install ply)
  - memory-profiler (to install: pip install memory_profiler)
  - matplotlib (to install: pip install matplotlib)
  - flask (to install: pip install flask)

pip install -r requirements.txt for install all dependencies

    (On a Debian-derived Linux distribution, e.g. Ubuntu, you can install the packages python3-sympy, python3-ply, python3-memory-profiler, and python3-mpltoolkits.basemap)

To launch server :
  - set FLASK_APP=app.py (Windows CMD) or export FLASK_APP=app.py (Unix Bash), see more : [http://flask.pocoo.org/docs/dev/cli/](http://flask.pocoo.org/docs/dev/cli/)
  - flask run

Get access :
  - http://127.0.0.1:5000/index
