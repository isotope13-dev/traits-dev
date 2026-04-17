#include <iostream>
#include <string>

namespace sample {

void log(const std::string& message) {
    std::cout << "[info] " << message << std::endl;
}

}  // namespace sample

int main() {
    sample::log("this sample does nothing");
    return 0;
}
