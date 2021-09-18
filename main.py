#!/usr/bin/python3
"""Proscan UI

Usage:
  main.py help
  main.py version
  main.py TOKEN REPO [--db=<database>] [--sdir=<schemadirectory>]

Arguments:
  TOKEN        The GitHub Token
  REPO         The fullname of a GitHub repository

Options:
    -h, help         Show help
    -v, version      Version
    --db=<database>  The SQLlite database file, by default is 'data/data.db'
    --sdir=<schemadirectory> The schema directory to find the corresponding DDL for table creation,\
                    by default is 'schemas'.
"""
from docopt import docopt
import gdump

def help():
    print(__doc__)

def version():
    print('Version %s' % gdump.__version__)

def execute(args):
    import os
    base_path=str(os.path.dirname(os.path.abspath(__file__)) ).replace(os.getcwd()+"/","")
    token = args.get('TOKEN')
    repo_fullname = args.get('REPO')
    extra_args = {"base_path":base_path}
    if args.get('--db'):
        extra_args['db_file'] = args.get('--db')
    if args.get('--sdir'):
        extra_args['schemas_dir'] = args.get('--sdir')
    gd = gdump.GitDump(token, repo_fullname, **extra_args)
    gd.sync_repo()

if __name__ == '__main__':
    args = docopt(__doc__, version=gdump.__version__)
    if args.get('help'):
        help()
    elif args.get('version'):
        version()
    else:
        execute(args)
    
