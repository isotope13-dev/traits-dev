// Static detection fixture. Never launches an instance; the client under
// test points at a local fake HTTP server and the test only asserts request
// serialization.
// Guards: an SDK client test that exercises the RunInstances operation with
// a UserData parameter against a loopback fake server is API simulation,
// never a remote-compute cryptojacking launch.
package ec2_test

import (
	"testing"

	"github.com/example/goamz/aws"
	"github.com/example/goamz/ec2"
	"github.com/example/goamz/testutil"
)

var testServer = testutil.NewHTTPServer()

func TestRunInstancesExample(t *testing.T) {
	testServer.Start()
	defer testServer.Flush()

	s := &S{ec2: ec2.New(
		aws.Auth{},
		aws.Region{EC2Endpoint: testServer.URL},
		testutil.DefaultClient,
	)}

	testServer.Response(200, nil, RunInstancesExample)

	options := ec2.RunInstances{
		ImageId:      "image-id",
		InstanceType: "t1.micro",
		UserData:     []byte("1234"),
	}

	resp, err := s.ec2.RunInstances(&options)
	if err != nil {
		t.Fatal(err)
	}

	req := testServer.WaitRequest()
	if got := req.Form["Action"]; len(got) != 1 || got[0] != "RunInstances" {
		t.Fatalf("unexpected action: %v", got)
	}
	if got := req.Form["UserData"]; len(got) != 1 || got[0] != "MTIzNA==" {
		t.Fatalf("unexpected user data: %v", got)
	}
	_ = resp
}
