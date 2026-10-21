use Test::More;
use Test::Mojo;
my $t = Test::Mojo->new('ExampleApp');
my $probe = '..::..::private::settings';
$t->get_ok("/doc/$probe")->status_is(404);
done_testing();
