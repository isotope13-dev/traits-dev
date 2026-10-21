public interface IFileOpenDialog { void Show(); }
public sealed class IndexerPicker {
    public int this[int index] { get => index; set { } }
    public string Executable => "ExampleService.exe";
}
