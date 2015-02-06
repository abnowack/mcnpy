# -*- coding: utf-8 -*-
"""
Created on Tue Jan 06 20:52:30 2015

@author: Aaron
"""
from datetime import datetime

class ptrac_header(object):
    ''' Parser and Python Represenation of PTRAC header '''
    
    def __init__(self, ptrac):
        line = ptrac.readline().strip()
        header_data = line.split()
        
        self.kod = header_data[0]
        self.ver = int(header_data[1])
        self.loddat = datetime.strptime(header_data[2], '%m/%d/%y')
        self.idtm = datetime.strptime('{0} {1}'.format(header_data[3],
                                      header_data[4]), '%m/%d/%y %H:%M:%S')
    
        self.aid = ptrac.readline().strip()
    
    def __str__(self):
        printstr = self.__class__.__name__
        for item in sorted(vars(self).items()):
            printstr += '\n  %s: %s' % item
        
        return printstr

class ptrac_input_format(object):
    ''' Parser and Python Representation of PTRAC Input Format '''
    
    def __init__(self, ptrac):
        line = ptrac.readline().strip() + ' ' + ptrac.readline().strip()
        in_fmt_data = [int(float(i)) for i in line.split()]

        i = 0
        self.n_keywords = in_fmt_data[i]
        i += 1
        
        keywords = ['buffer', 'cell', 'event', 'file', 'filter', 'max', 'menp',
                    'nps', 'surface', 'tally', 'type', 'value', 'write']
        for keyword in keywords:
            n_keys = in_fmt_data[i]
            i += 1
            self.__class__.__setattr__(self, keyword, in_fmt_data[i:i+n_keys])
            i += n_keys
    
    def __str__(self):
        printstr = self.__class__.__name__
        for item in sorted(vars(self).items()):
            printstr += '\n  %s: %s' % item
        
        return printstr

class ptrac_history(object):
    
    def __init__(self):
        self.events = []
    
    def __str__(self):
        printstr = self.__class__.__name__
        for item in sorted(vars(self).items()):
            if item[0] == 'events':
                printstr += '\n  %s : [' % item[0]
                for ev in item[1]:
                    printstr += '\n' + str(ev)
                printstr += '\n]'
            else:
                printstr += '\n  %s: %s' % item
        
        return printstr

class ptrac_event(object):
    def __init__(self):
        pass

    def __str__(self):
        printstr = self.__class__.__name__
        for item in sorted(vars(self).items()):
            printstr += '\n  %s: %s' % item
        
        return printstr

def parse_ptrac_events(ptrac, event_format):
    ''' Read and parse PTRAC events corresponding to the read format '''

    nps_format = ['nps', None, 'ncl', 'nsf', 'jptal', 'tal']
    evt_format = [None, 'node', 'nsr', 'nxs', 'ntyn', 'nsf', 'angsrf', 'nter',
                  'nbranch', 'ipt', 'ncl', 'mat', 'ncp', 'xxx', 'yyy', 'zzz', 
                  'uuu', 'vvv', 'www', 'erg', 'wgt', 'tme']
    
    int_list = lambda l: [int(a) for a in l]
    float_list = lambda l: [float(a) for a in l]
    
    line = ptrac.readline().strip()
    nps_data = int_list(line.split())
    
    next_event_type = nps_data[event_format.id_nps.index(2)]
    
    history = ptrac_history()
    for i, nps_var in enumerate(nps_data):
        nps_id = nps_format[event_format.id_nps[i]-1]
        if nps_id is None:
            continue
        history.__setattr__(nps_id, nps_var)
    
    # only for single evevnt, extend to multiple events
    while next_event_type != 9000:
        event_data = int_list(ptrac.readline().strip().split()) + \
                     float_list(ptrac.readline().strip().split())

        event = ptrac_event()
        (event.type, next_event_type) = (next_event_type, event_data[0])
        
        for i, ev_var in enumerate(event_data[1:]):
            if event.type / 1000 == 1: #src
                flags = event_format.id_src_ev
            elif abs(event.type / 1000) == 2: #bnk
                flags = event_format.id_bnk_ev
            elif event.type / 1000 == 3: #sur
                flags = event_format.id_src_ev
            elif event.type / 1000 == 4: #col
                flags = event_format.id_col_ev
            elif event.type / 1000 == 5: #ter
                pass
            else:
                pass
            ev_id = evt_format[flags[i]-len(nps_format)-1]
            if ev_id is None:
                continue
            event.__setattr__(ev_id, ev_var)
    
        history.events.append(event)
    
    return history

class ptrac_event_format(object):
    ''' Parser and Python Representation of PTRAC Event Format '''
    
    def __init__(self, ptrac):
        int_list = lambda l: [int(a) for a in l]
        # parse n variable line
        line = ptrac.readline().strip()
        n_ev_data = int_list(line.split())
        
        self.n_nps = n_ev_data[0]
        self.n_src_ev = sum(n_ev_data[1:3])
        self.n_bnk_ev = sum(n_ev_data[3:5])
        self.n_sur_ev = sum(n_ev_data[5:7])
        self.n_col_ev = sum(n_ev_data[7:9])
        self.n_ter_ev = sum(n_ev_data[9:11])
        self.ipt_single_transport = n_ev_data[11]
        self.output_byte_size = n_ev_data[12]
        
        # parse variable ids
        id_ev_data = []
        while len(id_ev_data) < sum(n_ev_data[:10]):
            line = ptrac.readline().strip()
            id_ev_data += line.split()
        
        i = 0
        self.id_nps = int_list(id_ev_data[:self.n_nps])
        i += self.n_nps
        self.id_src_ev = int_list(id_ev_data[i:i+self.n_src_ev])
        i += self.n_src_ev
        self.id_bnk_ev = int_list(id_ev_data[i:i+self.n_bnk_ev])
        i += self.n_bnk_ev
        self.id_sur_ev = int_list(id_ev_data[i:i+self.n_sur_ev])
        i += self.n_sur_ev
        self.id_col_ev = int_list(id_ev_data[i:i+self.n_col_ev])
        i += self.n_col_ev
        self.id_ter_ev = int_list(id_ev_data[i:i+self.n_ter_ev])
        
    def __str__(self):
        printstr = self.__class__.__name__
        for item in sorted(vars(self).items()):
            printstr += '\n %s: %s' % item
        
        return printstr
        
if __name__ == '__main__':
    ptrac = open('ptrac', 'r')
    
    # should always start with -1
    print ptrac.readline().strip()
    
    # ptrac header
    header = ptrac_header(ptrac)
    print header
    
    input_format = ptrac_input_format(ptrac)
    print input_format
    
    event_format = ptrac_event_format(ptrac)
    print event_format
    
    event_data = parse_ptrac_events(ptrac, event_format)
    
    ptrac.close()