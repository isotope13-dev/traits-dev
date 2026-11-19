document.querySelector('#share').addEventListener('click', async function () {
  await navigator.share({ title: document.title, url: location.href });
});
