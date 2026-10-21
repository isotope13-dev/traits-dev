package main
import("fmt"; "net"; "os"; "time")
func main(){
 fmt.Println("TCP port to probe; Provide IPs/CIDRs")
 if len(os.Args)!=2{return}
 ip,n,e:=net.ParseCIDR(os.Args[1]);if e!=nil{return}
 ip=ip.To4();if ip==nil{return}
 for ip=n.IP.To4();n.Contains(ip);{
  c,e:=net.DialTimeout("tcp",net.JoinHostPort(ip.String(),"445"),time.Second)
  if e==nil{fmt.Println(ip);c.Close()}
  for i:=len(ip)-1;i>=0;i--{ip[i]++;if ip[i]!=0{break}}
 }
}
