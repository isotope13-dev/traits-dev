// Download-manager companion content script (benign control): intercepts
// clicks only on file-download anchors and hands the URL to the native
// downloader through the background worker. The download-attribute gate is
// what separates this from a link-click hijacker.
(function () {
  'use strict'

  const DOWNLOAD_EXTS = new Set(['zip', 'rar', '7z', 'exe', 'dmg', 'iso'])

  const isDownloadLink = (a) => {
    if (a.hasAttribute('download')) return true
    const href = a.getAttribute('href') || ''
    const ext = (href.split('.').pop() || '').toLowerCase().split(/[?#]/)[0]
    return DOWNLOAD_EXTS.has(ext)
  }

  document.addEventListener('click', (event) => {
    if (event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return
    const link = event.target.closest('a')
    if (!link) return
    if (!isDownloadLink(link)) return
    const url = new URL(link.getAttribute('href'), window.location.href).href
    event.preventDefault()
    event.stopImmediatePropagation()
    chrome.runtime.sendMessage({ type: 'downloadUrl', url: url }, () => {})
  }, true)
})()
