# -*- coding: utf-8 -*-
"""
Created on Tue Jan 06 20:52:30 2015

@author: Aaron

Notes:
nbranch only seems to appear on termination event
in n,Xn reactions bank events are created
"""
from datetime import datetime

class ptrac_header(object):
    ''' Parser and Python Represenation of PTRAC header '''
    
    def __init__(self, ptrac):
        line = ptrac.readline().strip()
        if line == '-1':
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
        line = ptrac.readline().strip()
        in_fmt_data = [int(float(i)) for i in line.split()]

        i = 0
        self.n_keywords = in_fmt_data[i]
        i += 1
        
        keywords = ['buffer', 'cell', 'event', 'file', 'filter', 'max', 'menp',
                    'nps', 'surface', 'tally', 'type', 'value', 'write']
        for keyword in keywords:
            # if reach end of in_fmt_data, there is another line to read
            if i >= len(in_fmt_data):
                line = ptrac.readline().strip()
                in_fmt_data += [int(float(j)) for j in line.split()]
            n_keys = in_fmt_data[i]
            if i+n_keys >= len(in_fmt_data):
                line = ptrac.readline().strip()
                in_fmt_data += [int(float(j)) for j in line.split()]
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
    
    __ntyn_rxn = {}
    
    def __init__(self):
        pass

    def __str__(self):
        printstr = self.__class__.__name__
        for item in sorted(vars(self).items()):
            printstr += '\n  %s: %s' % item
        
        return printstr

def parse_ptrac_events(ptrac, event_format):
    ''' Read and parse PTRAC events corresponding to the read format
    
        NPS LINE
        ========
        NPS = Source particle count
        NCL = Problem number of the cells
        NSF = Problem number of the surfaces
        JPTAL = Basic tally information
        TAL = Tally scores accumulation
        
        EVENT LINE
        ==========        
        NODE = Number of nodes in track from source to here
        NSR = Source type
        NXS = Blocks of descriptors of cross-section tables
        NTYN = Type of reaction in current collision
        NSF = Surface Number
        ANGSRF = Angle with surface normal (degrees)
        NTER = Termination Type
        NBRANCH = Branch number for this history
        IPT = Type of particle (1=neutron, 2=photon, 0=others)
        NCL = Problem number of the cells
        MAT = Material number of the cells
        NCP = Count of collisions per track
        XXX = X-coordinate of particle position
        YYY = Y-coordinate of particle position
        ZZZ = Z-coordinate of particle position
        UUU = Particle direction cosine with X-axis
        VVV = Particle direction cosine with Y-axis
        WWW = Particle direction cosine with Z-axis
        ERG = Particle energy
        WGT = Particle weight
        TME = Time at the particle position
        
        TYPE
        ====
        1000   = SRC
        2000+L = BANK
        3000   = SURFACE
        4000   = COLLISION
        5000   = TERMINATION
    '''

    format_ = ['nps', None, 'ncl', 'nsf', 'jptal', 'tal', None, 'node', 'nsr',
               'nxs', 'ntyn', 'nsf', 'angsrf', 'nter', 'nbranch', 'ipt', 'ncl',
               'mat', 'ncp', 'xxx', 'yyy', 'zzz', 'uuu', 'vvv', 'www', 'erg',
               'wgt', 'tme']
    
    int_list = lambda l: [int(a) for a in l]
    float_list = lambda l: [float(a) for a in l]
    
    while True:
        line = ptrac.readline().strip()
        nps_data = int_list(line.split())
        
        if len(nps_data) == 0:
            return
        
        next_event_type = nps_data[event_format.id_nps.index(2)]
        
        history = ptrac_history()
        for i, nps_var in enumerate(nps_data):
            nps_id = format_[event_format.id_nps[i]-1]
            if nps_id is None:
                continue
            history.__setattr__(nps_id, nps_var)
        
        while next_event_type != 9000:
            event_data = float_list(ptrac.readline().strip().split()) + \
                         float_list(ptrac.readline().strip().split())
    
            event = ptrac_event()
            (event.type, next_event_type) = (next_event_type, event_data[0])
    
            if event.type / 1000 == 1: #src
                flags = event_format.id_src_ev
            elif abs(event.type / 1000) == 2: #bnk
                flags = event_format.id_bnk_ev
            elif event.type / 1000 == 3: #sur
                flags = event_format.id_sur_ev
            elif event.type / 1000 == 4: #col
                flags = event_format.id_col_ev
            elif event.type / 1000 == 5: #ter
                flags = event_format.id_ter_ev
            else:
                pass
            
            for i, ev_var in enumerate(event_data):
                ev_id = format_[flags[i]-1]
                if ev_id is None:
                    continue
                event.__setattr__(ev_id, ev_var)
        
            history.events.append(event)
        
        yield history

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
    with open('example/ptrac', 'r') as ptrac:
        # ptrac header
        header = ptrac_header(ptrac)
        print header
        
        input_format = ptrac_input_format(ptrac)
        print input_format
        
        event_format = ptrac_event_format(ptrac)
        print event_format
        
        event_data = parse_ptrac_events(ptrac, event_format)
        print event_data
