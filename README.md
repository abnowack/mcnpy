# ptrac_reader
Reader for MCNP6 PTRAC files

![event](example/event.png?raw=true)

Supports ASCII files for MCNP6 currently

Parse the header, input format, and event format. Then pass the event format to the ptrac event parser.

Example
```python
from ptrac_reader import *

ptrac = open('ptrac', 'r')

# should be -1
print ptrac.readline().strip()
# parse headers and formats
header = ptrac_header(ptrac)
input_format = ptrac_input_format(ptrac)
event_format = ptrac_event_format(ptrac)
# parse a single event
history = parse_ptrac_events(ptrac, event_format)
# print first particle track
print history.events[0]

ptrac.close()
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

ptrac_plotter.py shows how to plot events for display as shown above
