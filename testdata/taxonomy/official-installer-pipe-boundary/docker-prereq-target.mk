docker:
	apt-get -qq -y --no-install-recommends install curl
	wget -nv -O - https://get.docker.com/ | sh
	sleep 2
