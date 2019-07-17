"""
.. module:: restapi

  :platform: Unix, Windows

  :synopsis: This module implements the REST API used to interact with the test case. The API is implemented using the ``flask`` package. 

.. moduleauthor:: Sen Huang
"""
# -*- coding: utf-8 -*-
"""
This module implements the REST API used to interact with the test case.  
The API is implemented using the ``flask`` package.  
"""

#try:
# GENERAL PACKAGE IMPORT
# ----------------------
from flask import Flask
from flask_restful import Resource, Api, reqparse
# ----------------------

# TEST CASE IMPORT
# ----------------
from testcase import TestCase
# ----------------
#except ImportError:
#    pass

# DEFINE REST REQUESTS
# --------------------
class Advance(Resource):
    '''Interface to advance the test case simulation.'''    
    
    def post(self):
        '''POST request with input data to advance the simulation one step 
        and receive current measurements.'''
        u = parser_advance.parse_args()
        # print u
        y = case.advance(u)
        # print y
        yCelsius = y['TOutDryBul_y'] - 273.15
        # print 'Outside temperature: {0} deg Kelvin ({1} deg Celsius).'.format(y['TOutDryBul_y'], yCelsius)
        return y

class Reset(Resource):
    '''Interface to test case simulation step size.'''
    
    def put(self):
        '''PUT request to reset the test.'''
        u = parser_reset.parse_args()
        # print 'yes'
        # print u
        start=u['start']
        case.reset(start)
        return 'Testcase reset.'

        
class Step(Resource):
    '''Interface to test case simulation step size.'''
    
    def get(self):
        '''GET request to receive current simulation step in seconds.'''
        step = case.get_step()
        return step

    def put(self):
        '''PUT request to set simulation step in seconds.'''
        args = parser_step.parse_args()
        # print args
        step = args['step']
        case.set_step(step)
        return step, 201
        
class Inputs(Resource):
    '''Interface to test case inputs.'''
    
    def get(self):
        '''GET request to receive list of available inputs.'''
        u_list = case.get_inputs()
        return u_list
        
class Measurements(Resource):
    '''Interface to test case measurements.'''
    
    def get(self):
        '''GET request to receive list of available measurements.'''
        y_list = case.get_measurements()
        return y_list
        
class Results(Resource):
    '''Interface to test case result data.'''
    
    def get(self):
        '''GET request to receive measurement data.'''
        Y = case.get_results()
        return Y
        
class KPI(Resource):
    '''Interface to test case KPIs.'''
    
    def get(self):
        '''GET request to receive KPI data.'''
        kpi = case.get_kpis()
        return kpi
        
class Name(Resource):
    '''Interface to test case name.'''
    
    def get(self):
        '''GET request to receive test case name.'''
        name = case.get_name()
        return name
# --------------------
        
if __name__ == '__main__':
    # FLASK REQUIREMENTS
    # ------------------
    app = Flask(__name__)
    api = Api(app)
    # ------------------

    # INSTANTIATE TEST CASE
    # ---------------------
    case = TestCase()
    # ---------------------

    # DEFINE ARGUMENT PARSERS
    # -----------------------
    # ``step`` interface
    parser_step = reqparse.RequestParser()
    parser_step.add_argument('step')
    # ``reset`` interface
    parser_reset = reqparse.RequestParser()
    parser_reset.add_argument('start')
    # ``advance`` interface
    parser_advance = reqparse.RequestParser()
    for key in case.u.keys():
        parser_advance.add_argument(key)
    # -----------------------

    # ADD REQUESTS TO API WITH URL EXTENSION
    # --------------------------------------
    api.add_resource(Advance, '/advance')
    api.add_resource(Reset, '/reset')
    api.add_resource(Step, '/step')
    api.add_resource(Inputs, '/inputs')
    api.add_resource(Measurements, '/measurements')
    api.add_resource(Results, '/results')
    api.add_resource(KPI, '/kpi')
    api.add_resource(Name, '/name')
    # --------------------------------------

    app.run(debug=False, host='0.0.0.0')