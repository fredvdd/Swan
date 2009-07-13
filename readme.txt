Stage# - http://www.doc.ic.ac.uk/~cmz05/stage

Stage# was created by Chris Zetter
It is based on Stage which was created by John Ayres

Stage# is free for non-commercial use/modification with
attribution.

-----------------------------------------------------------

Managers require python 2.6, Theatres can use python 2.5.
Use of the Visualiser requires the svgfig python module,
see: http://code.google.com/p/svgfig/

To use Stage# (on a unix-like system):

Add the 'stage' directory to your $PYTHONPATH variable.

Then from the 'stage' directory managers can be started by:
python Manager/manager.py

A manager can join an existing Stage# system by giving it
the host:port of any manager already in the system, for 
example:
python Manager/manager.py 100.100.100.100:7000

Any Stage# script can be run using python on a host where a
manager is running. The settings in host/setting.py must be
changed if you wish to use a non-local manager or one not
on the default port (7000).
