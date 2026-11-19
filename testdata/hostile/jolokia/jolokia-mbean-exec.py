import requests

BASE = 'http://target.example:8161'


def set_logger_config(session, mbean, template):
    session.post(BASE + '/api/jolokia/', json=dict(
        type='exec',
        mbean=mbean,
        operation='setConfigText',
        arguments=[template, 'utf-8'],
    ))
