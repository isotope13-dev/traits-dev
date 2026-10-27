using System.Diagnostics;
class InputDriverConfiguration {
    static void Main() {
        Process.Start("sc", "config i8042prt start= demand");
    }
}
