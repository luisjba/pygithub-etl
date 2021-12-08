#!/usr/bin/python3
"""GithubETL Library

Usage:
  main.py help
  main.py version
  main.py sync TOKEN REPO [--db=<database>] [--sdir=<schemadirectory>]
  main.py analize [--db=<database>]
  main.py dashboard [--db=<database>]

Arguments:
  TOKEN        The GitHub Token
  REPO         The fullname of a GitHub repository

Options:
    -h, help         Show help
    -v, version      Version
    -f, force_update Force the update of commit and files
    --db=<database>  The SQLlite database file, by default is 'data/data.db'
    --sdir=<schemadirectory> The schema directory to find the corresponding DDL for table creation,\
by default is 'schemas'.
"""
from docopt import docopt
import flask
import etl
import os
from socket import gethostname

def _get_base_path() -> str:
    return str(os.path.dirname(os.path.abspath(__file__)) ).replace(os.getcwd()+"/","")

def help():
    print(__doc__)

def version():
    print('Version %s' % etl.__version__)

def sync(args:dict):
    token = args.get('TOKEN')
    repo_fullname = args.get('REPO')
    extra_args = {"base_path":_get_base_path()}
    if args.get('--db'):
        extra_args['db_file'] = args.get('--db')
    if args.get('--sdir'):
        extra_args['schemas_dir'] = args.get('--sdir')
    getl = etl.GithubETL(token, repo_fullname, **extra_args)
    getl.sync_repo()
    getl.sync_branches()
    getl.sync_commits(args.get('--force_update', False))

def analize(args):
    print("TODO: ANALIZE")

def dashboard(args) -> flask.Flask:
    run_kargs={
        "port":5000,
        "debug":True
    }
    dashboard_kargs={
        "db_path": os.path.join(
                        _get_base_path(), 
                        args.get('--db') if args.get('--db') else "data/data.db"
                    )
    }
    app = etl.dashboard_app(**dashboard_kargs)
    if not args.get('--not_run'):
        app.run(**run_kargs)
    else:
        return app

if __name__ == '__main__':
    # Check if a uWSGY mode is executing them
    if 'liveconsole' in gethostname():
        app = dashboard({'--not_run':True})
        # dashboard({})
    else:
        args = docopt(__doc__, version=etl.__version__)
        #print(args)
        if args.get('help'):
            help()
        elif args.get('version'):
            version()
        elif  args.get('analize'):
            analize(args)
        elif  args.get('sync'):
            sync(args)
        elif  args.get('dashboard'):
            dashboard(args)
        else:
            print("Invalid command")
            help()
    
