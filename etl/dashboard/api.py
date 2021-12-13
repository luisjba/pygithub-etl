import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from .db import (
    repos_modified_series, repos_modified_files_series,
    commits_max_date, repos_modified_by_author_series,
    repos_top_contributors, repos_top_contributors_by_repo
)

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/modified', defaults={"start":0,"end":0}, methods=('GET', 'POST'))
@bp.route('/modified/<int:start>', defaults={"end":0}, methods=('GET', 'POST'))
@bp.route('/modified/<int:start>/<int:end>', methods=('GET', 'POST'))
def modified(start, end):
    series = repos_modified_series(start, end)
    return jsonify({
        'series':[
            {
                'name':'Repos',
                'ColorByPoint':1,
                'data':[
                    {
                        "name":s['Name'],
                        "y":s['Total'],
                        "drilldown":s['Id']
                    } 
                    for s in series]
            }
        ],
        'drilldown_series':[]
    })

@bp.route('/files', defaults={"start":0,"end":0}, methods=('GET', 'POST'))
@bp.route('/files/<int:start>', defaults={"end":0}, methods=('GET', 'POST'))
@bp.route('/files/<int:start>/<int:end>', methods=('GET', 'POST'))
def files(start, end):
    series = repos_modified_files_series(start, end)
    return jsonify({
        'series':[
            {
                'name':'Repos',
                'ColorByPoint':1,
                'data':[
                    {
                        "name":s['Name'],
                        "y":s['Total'],
                        "drilldown":s['Id']
                    } 
                    for s in series]
            }
        ],
        'drilldown_series':[]
    })

@bp.route('/author', defaults={"start":0,"end":0}, methods=('GET', 'POST'))
@bp.route('/author/<int:start>', defaults={"end":0}, methods=('GET', 'POST'))
@bp.route('/author/<int:start>/<int:end>', methods=('GET', 'POST'))
def author(start, end):
    series = repos_modified_by_author_series(start, end)
    return jsonify({
        'series':[
            {
                'name':'Repos',
                'ColorByPoint':1,
                'data':[
                    {
                        "name":s['Name'],
                        "y":s['Total'],
                        "drilldown":s['Id']
                    } 
                    for s in series]
            }
        ],
        'drilldown_series':[]
    })

@bp.route('/contributors', defaults={"start":0,"end":0,"limit":10}, methods=('GET', 'POST'))
@bp.route('/contributors/<int:start>', defaults={"end":0,"limit":10}, methods=('GET', 'POST'))
@bp.route('/contributors/<int:start>/<int:end>', defaults={"limit":10}, methods=('GET', 'POST'))
@bp.route('/contributors/<int:start>/<int:end>/<int:limit>', methods=('GET', 'POST'))
def contributors(start, end, limit):
    contributors = repos_top_contributors(start, end, limit=limit)
    return jsonify({
        'contributors': [
            {
                "name":c['name'],
                "login":c['login'],
                "url":c['url'],
                "contributions":c['contributions'],
                "contributions_str":"{:,}".format(c['contributions']),
                "repos":c['repos'],
                "repos_str":"{:,}".format(c['repos']),
                "files":c['files'],
                "files_str":"{:,}".format(c['files'])
            } 
            for c in contributors
        ]
    })

@bp.route('/contributorsbyrepo', 
    defaults={"repo":0,"start":0,"end":0,"limit":10,"order_by":'contributions'}, 
    methods=('GET', 'POST'))
@bp.route('/contributorsbyrepo/<int:repo>', 
    defaults={"start":0,"end":0,"limit":10,"order_by":'contributions'}, 
    methods=('GET', 'POST'))
@bp.route('/contributorsbyrepo/<int:repo>/<int:start>', 
    defaults={"end":0,"limit":10,"order_by":'contributions'}, methods=('GET', 'POST'))
@bp.route('/contributorsbyrepo/<int:repo>/<int:start>/<int:end>', defaults={"limit":10,"order_by":'contributions'}, 
    methods=('GET', 'POST'))
@bp.route('/contributorsbyrepo/<int:repo>/<int:start>/<int:end>/<int:limit>/<string:order_by>', 
    methods=('GET', 'POST'))
def contributors_by_repo(repo, start, end, limit, order_by):
    contributors = repos_top_contributors_by_repo(repo, start, end, limit=limit, order_by=order_by)
    return jsonify({
        'contributors': [
            {
                "name":c['name'],
                "login":c['login'],
                "url":c['url'],
                "contributions":c['contributions'],
                "contributions_str":"{:,}".format(c['contributions']),
                "repos":c['repos'],
                "repos_str":"{:,}".format(c['repos']),
                "files":c['files'],
                "files_str":"{:,}".format(c['files'])
            } 
            for c in contributors
        ]
    })