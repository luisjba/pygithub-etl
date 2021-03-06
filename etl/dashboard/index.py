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
            'enpoint': url_for('api.modified'),
            'order_by':'contributions',
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
            'enpoint': url_for('api.files'),
            'order_by':'files',
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
            'enpoint': url_for('api.author'),
            'order_by':'contributions',
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
        end_date=max_date,
        contributors_endpoint= url_for('api.contributors')
    )