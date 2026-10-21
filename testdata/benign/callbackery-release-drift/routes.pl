use Mojolicious::Lite;
my $routes = app->routes;
$routes->get('/login')->to(cb => sub { shift->render(text => 'Sign in') });
$routes->post('/login')->to(cb => sub { shift->render(text => 'Done') });
