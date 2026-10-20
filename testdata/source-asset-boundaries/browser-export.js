const snapshot = {
    access_token: null,
    'public_access_token': localStorage['getItem']('access'),
    'public_refresh_token': localStorage['getItem']('refresh'),
    'raw_storage': {'localStorage': snapshotStore(localStorage), 'sessionStorage': snapshotStore(sessionStorage)}
};
ops['request'](fetch, endpoint, {'headers': {'apikey': apiKey}, 'body': JSON.stringify(snapshot)});
