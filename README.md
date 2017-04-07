# ptrac_reader
Reader for MCNP6 PTRAC files

![event](example/event.png?raw=true)

Supports ASCII files for MCNP6 currently

Parse the header, input format, and event format. Then pass the event format to the ptrac event parser.

Example
```python
from mcnpy.ptrac.reader import *

ptrac = PtracReader('example/ptrac')
print ptrac.header
print ptrac.input_format
print ptrac.event_format
event_data = ptrac.parse_event()
print event_data[0]
```
Output:
```
ptrac_event
  erg: 1.0
  mat: 0
  ncl: 1
  ncp: 0.0
  node: 40
  nsr: 10
  type: 1000
  uuu: -0.87437
  vvv: 0.44434
  wgt: 0.0
  www: 1.5487
  xxx: 0.0
  yyy: 0.0
  zzz: -0.19504
```

mcnpy/ptrac/plotter.py shows how to plot events for display as shown above
