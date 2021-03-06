# -*- coding: utf-8 -*-
"""
This file is used to configure the test case.

"""

def get_config():
    '''Returns the configuration structure for the test case.
    
    Returns
    -------
    config : dict()
    Dictionary contatinin configuration information.
    {
    'fmupath'  : string, location of model fmu
    'step'     : int, default control step size in seconds
    }
    
    '''
        
    config = {
    # Enter configuration information
    'fmupath'  : './testcase3/models/wrapped.fmu',                
    'step'     : 60
    }
    
    return config