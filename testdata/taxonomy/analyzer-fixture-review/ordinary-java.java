import java.util.Collections;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
class Ordinary {
  boolean equals(Object other) { return this == other; }
  void addMethod() {}
  void transform() {}
  void selfModify() {}
  void run(java.util.List<String> list, HttpServletRequest request) {
    Collections.reverse(list);
    request.getParameter("name");
    java.util.Base64.getDecoder();
  }
  @PostMapping("/example")
  void post(@RequestParam String value) {}
}
