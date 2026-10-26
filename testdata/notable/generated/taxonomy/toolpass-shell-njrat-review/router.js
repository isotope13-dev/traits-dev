function selectTab(tab) {
  history.replaceState({tab}, '', '/tabs/' + encodeURIComponent(tab));
}
