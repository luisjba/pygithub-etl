#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard , Flask Appication
@datecreated: 2021-11-18
@lastupdated: 2021-11-18
@author: Jose Luis Bracamonte Amavizca
"""
# Meta informations.
__author__ = 'Jose Luis Bracamonte Amavizca'
__version__ = '0.1.2'
__maintainer__ = 'Jose Luis Bracamonte Amavizca'
__email__ = 'me@luisjba.com'
__status__ = 'Development'

import os
from flask import Flask, blueprints
from flask_bootstrap import Bootstrap
from . import db, index, details, api

def create_app(test_config=None, db_path = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Bootstraping the app
    Bootstrap(app)

    if db_path is None:
        db_path = os.path.join(app.instance_path, 'flaskr.sqlite')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=db_path,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register db init into the app
    db.init_app(app)

    # Blueprint registration
    blueprints_list = [index, details, api]
    for bp_item in blueprints_list:
        app.register_blueprint(bp_item.bp)
    return app

