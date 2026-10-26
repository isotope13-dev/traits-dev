package rediscontrols

// Static analyzer control. Never build or run this fixture.
// Redis-style pub/sub calls without any NATS import: the generic
// Publish/Subscribe call shapes must not read as NATS usage.

// Client mirrors the go-redis call surface used in its own tests.
type Client struct{}

func (c *Client) Publish(channel string, message string) error { return nil }

func (c *Client) Subscribe(channel string) error { return nil }

func Example() {
	var c Client
	_ = c.Publish("mychannel1", "hello")
	_ = c.Subscribe("mychannel1")
}
