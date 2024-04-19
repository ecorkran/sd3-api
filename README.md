# sd3-api

Stable Diffusion 3 API example program.  Currently runs as a Python module.
Run from a virtual environment.  Minimal instructions here, assuming pip.

##### Preliminary Instructions

* clone from github
* todo: add instructions for downloading from github
* create virtual environment
```
python -m venv .venv
```

* activate virtual environment
```
   source .venv/bin/activate   -- linux
   call .venv/Scripts/activate -- windows
```

* run as module:
```
python -m src.sd3 --help
```

##### Notes
* you will need a (free) API key from stability.ai.
* Includes 25 credits.  After that credits are $0.01 each,
* in units of $10.  SD3 image costs 6.5 cents to generate.
