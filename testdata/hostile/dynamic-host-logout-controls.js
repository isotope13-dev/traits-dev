// Query-chosen logout destination: the host comes from the URL query string,
// not from operator configuration, and no Amplify SDK markers are present.
// The suspicious dynamic-host logout template must still fire here.
const target = new URLSearchParams(location.search).get('host');
const logoutUrl = `https://${target}/logout?session=${sid}`;
frames[0].location = logoutUrl;
