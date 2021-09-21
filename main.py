#!/usr/bin/python3
"""Proscan UI

Usage:
  main.py help
  main.py version
  main.py sync TOKEN REPO [--db=<database>] [--sdir=<schemadirectory>]
  main.py analize [--db=<database>]

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
import etl

def _get_base_path() -> str:
    import os
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
    gd = etl.GithubETL(token, repo_fullname, **extra_args)
    gd.sync_repo()
    gd.sync_branches()
    gd.sync_commits(args.get('--force_update', False))

def analize(args):
    print("TODO: ANALIZE")


if __name__ == '__main__':
    args = docopt(__doc__, version=etl.__version__)
    print(args)
    if args.get('help'):
        help()
    elif args.get('version'):
        version()
    elif  args.get('analize'):
        analize(args)
    else:
        sync(args)
    
