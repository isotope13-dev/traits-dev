package monitor
import (
    "context"
    "github.com/spf13/cobra"
    "github.com/bishopfox/sliver/client/console"
    "github.com/bishopfox/sliver/protobuf/commonpb"
)
func request(cmd *cobra.Command, con *console.SliverClient, args []string) {
    var err error
    _, err = con.Rpc.MonitorStop(context.Background(), &commonpb.Empty{})
    _ = err
}
