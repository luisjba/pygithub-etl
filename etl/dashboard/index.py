import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from .db import (
    repos_modified_series, repos_modified_files_series,
    commits_max_date, repos_modified_by_author_series,
    repos_top_contributors
)

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    max_date = commits_max_date()
    chart_list = [
        {
            'id':'topModified',
            'enpoint': url_for('index.modified'),
            'chart_options':{
                'chart':{'type':'bar'},
                'title': {'text':'Changes'},
                'yAxis':{
                    'title':{
                        'text':'Total changes'
                    }
                }
            }
        },
        {
            'id':'topModifiedFiles',
            'enpoint': url_for('index.files'),
            'chart_options':{
                'chart':{'type':'bar'},
                'title': {'text':'Files Modified'},
                'yAxis':{
                    'title':{
                        'text':'Files Modified'
                    }
                }
            }
        },
        {
            'id':'topModifiedByAuthor',
            'enpoint': url_for('index.author'),
            'chart_options':{
                'chart':{'type':'bar'},
                'title': {'text':'Contributors'},
                'yAxis':{
                    'title':{
                        'text':'Files Modified'
                    }
                }
            }
        }
    ]
    return render_template(
        'index/index.html',
        chart_list=chart_list,
        start_date=max_date - (7 * 60_000),
        end_date=max_date
    )

@bp.route('/modified', defaults={"start":0,"end":0}, methods=('GET', 'POST'))
@bp.route('/modified/<int:start>/', defaults={"end":0}, methods=('GET', 'POST'))
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
                        "drilldown":s['Name']
                    } 
                    for s in series]
            }
        ],
        'drilldown_series':[]
    })

@bp.route('/files', defaults={"start":0,"end":0}, methods=('GET', 'POST'))
@bp.route('/files/<int:start>/', defaults={"end":0}, methods=('GET', 'POST'))
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
                        "drilldown":s['Name']
                    } 
                    for s in series]
            }
        ],
        'drilldown_series':[]
    })

@bp.route('/author', defaults={"start":0,"end":0}, methods=('GET', 'POST'))
@bp.route('/author/<int:start>/', defaults={"end":0}, methods=('GET', 'POST'))
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
                        "drilldown":s['Name']
                    } 
                    for s in series]
            }
        ],
        'drilldown_series':[]
    })

@bp.route('/contributors', defaults={"start":0,"end":0}, methods=('GET', 'POST'))
@bp.route('/contributors/<int:start>/', defaults={"end":0}, methods=('GET', 'POST'))
@bp.route('/contributors/<int:start>/<int:end>', methods=('GET', 'POST'))
def contributors(start, end):
    return jsonify({
        'contributors': repos_top_contributors(start, end)
    })