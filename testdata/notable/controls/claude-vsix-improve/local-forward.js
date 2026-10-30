const options="ssh -N -L 44022:localhost:22 -o StrictHostKeyChecking=no";
const loop="while true; do ssh target; sleep 17; done";
