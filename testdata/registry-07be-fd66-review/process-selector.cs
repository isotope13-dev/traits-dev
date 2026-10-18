class ProcessSelector {
    string GetCreateProcessFunction(int selector) {
        return selector == 0 ? "CreateProcessWithLogonW" : "CreateProcessWithTokenW";
    }
}
