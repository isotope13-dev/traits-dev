function renderTotal(items) {
  var total = 0;
  for (var i = 0; i < items.length; i++) {
    total += items[i].price * items[i].qty;
  }
  document.getElementById("total").textContent = String(total);
}
