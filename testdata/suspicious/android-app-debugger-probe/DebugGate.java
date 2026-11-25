package com.example.game;

import android.os.Debug;

/** Refuses to run its routine while a debugger is attached. */
public final class DebugGate {
    private DebugGate() {}

    public static boolean allowed() {
        return !Debug.isDebuggerConnected();
    }
}
