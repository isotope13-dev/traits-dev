const rule = {
  action: {
    type: "modifyHeaders",
    requestHeaders: [{ header: "Origin", operation: "remove" }],
  },
  condition: { urlFilter: "https://collector.example/*" },
};
