class Notification {
  void apply(Builder builder, Object payload) { builder.setBody(payload); }
  Object text(Content content) { return content.getText(); }
}
