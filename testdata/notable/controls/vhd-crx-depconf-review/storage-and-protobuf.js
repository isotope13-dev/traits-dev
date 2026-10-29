chrome.storage.local.get(null, handleLoaded);
chrome.storage.local.set({targetLang: 'en'});
MutableTranslateTextResponse.prototype.removeDefinitions = function(index) {
  return removeFromRepeatedWrapperField(this,18,DefinitionResult,index);
};
const shared = new SharedWorker('translation.js');
