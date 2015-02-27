# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 11:29:31 2015

@author: Aaron
"""

import subprocess
import tempfile
import shutil
from contextlib import contextmanager

def clean_directory(clean_dir):
    shutil.rmtree(clean_dir)

@contextmanager
def run_mcnp(card, params={}, cores=1, clean=True, **kwargs):
    card = card.format(**params)
    
    args = ['tasks', cores]
    
    # create temp folder
    output_dir = tempfile.mkdtemp(dir='.')
    with open(output_dir + '\\input.i', 'w') as f:
        f.write(card)
    
    args += ['i=input.i']

    # mcnp doesn't use errorcodes or stderr, so Popen doesnt add features
    # stick with simpler check_output and parse stdout
    args = [str(i) for i in args]
    mcnp = subprocess.check_output(['mcnp6'] + args, shell=True,
                                   cwd=output_dir)
    
    # check for errors in stdout
    if 'bad trouble' in mcnp or 'fatal error' in mcnp:
        print 'Error in MCNP outout'
        print mcnp
        status = False
    else:
        status = True
    
    try:
        yield status, output_dir
    finally:
        if clean:
            clean_directory(output_dir)
            
#    return status, output_dir