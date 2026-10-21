package main
import("fmt";"net";"os";"time")
func main(){ fmt.Println("CIDR targets; address parser"); if len(os.Args)>1{c,e:=net.DialTimeout("tcp",os.Args[1],time.Second); if e==nil{c.Close()}} }
