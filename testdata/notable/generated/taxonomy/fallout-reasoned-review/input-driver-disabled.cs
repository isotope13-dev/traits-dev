using System.Diagnostics;
class InputDriverConfiguration {
    static void Main() {
        Process.Start("sc", "config i8042prt start= disabled");
        Process.Start("sc", "stop i8042prt");
    }
}
