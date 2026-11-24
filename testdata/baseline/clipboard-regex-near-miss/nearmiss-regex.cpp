#include <regex>
#include <string>
void f(std::string input){
  std::regex re("a+");
  if (std::regex_match(input, re)) {}
}
