package supervisor

func start() {
	env := strings.Join(os.Environ(), "\n")
	launchChild(env)
	http.PostForm(endpoint, url.Values{"status": {"ready"}})
}
