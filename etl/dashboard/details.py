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

bp = Blueprint('details', __name__, url_prefix='/details')
@bp.route('/')
def index():
    max_date = commits_max_date()
    chart_list = [
        {
            'id':'topModified',
            'endpoint': url_for('api.modified'),
            'order_by':'contributions',
            'drilldownEndpoint': url_for('api.contributors_by_repo'),
            'chart_options':{
                'chart':{'type':'bar'},
                'title': {'text':'Changes'},
                'yAxis':{
                    'title':{
                        'text':'Total changes'
                    }
                },
                'xAxis':{
                    'type': 'category'
                }
            }
        },
        {
            'id':'topModifiedFiles',
            'endpoint': url_for('api.files'),
            'order_by':'files',
            'drilldownEndpoint': url_for('api.contributors_by_repo'),
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
            'endpoint': url_for('api.author'),
            'order_by':'contributions',
            'drilldownEndpoint': url_for('api.contributors_by_repo'),
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
        'details/index.html',
        chart_list=chart_list,
        start_date=max_date - (7 * 60_000),
        end_date=max_date,
        contributors_endpoint= url_for('api.contributors')
    )

