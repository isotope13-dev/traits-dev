package main

import (
	"k8s.io/klog/v2"
)

func main() {
	klog.InitFlags(nil)
	defer klog.Flush()
	klog.Info("this does app nothing")
}
