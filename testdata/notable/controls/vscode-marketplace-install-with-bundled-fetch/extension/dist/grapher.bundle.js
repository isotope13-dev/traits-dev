function loadChartDefinition(url) {
  return fetch(url).then(response => response.text());
}

module.exports = { loadChartDefinition };
