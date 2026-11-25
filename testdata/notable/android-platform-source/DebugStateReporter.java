/*
 * Copyright (C) 2008 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 */

package com.android.server;

import android.os.Debug;

/** @hide Framework diagnostics for the system server. */
public final class DebugStateReporter {
    private DebugStateReporter() {}

    /** Reports whether a debugger is attached to the system server. */
    public static String describe() {
        if (Debug.isDebuggerConnected()) {
            return "Debugger: Connected";
        }
        return "Debugger: none";
    }
}
