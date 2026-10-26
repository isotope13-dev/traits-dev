CKEDITOR.dialog.add("about", function (a) {
  return { title: CKEDITOR.env.ie ? a.dlgTitle : a.title, minWidth: 390 };
});
var plain = { title: SOME_TITLE, text: SOME_TEXT };
