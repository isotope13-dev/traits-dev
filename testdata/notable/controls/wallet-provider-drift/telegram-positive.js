const TelegramBot = require("node-telegram-bot-api");
const service = new TelegramBot(process.env.BOT_TOKEN, {polling: true});
service.onText(/ping/, () => service.sendMessage(user, "pong"));
