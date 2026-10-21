public interface IFileOpenDialogEvents { void OnSelectionChange(); }
public sealed class ItemsEnabled {
    public bool ItemsEnabledFlag { get; set; }
    public void set_ItemsEnabled(bool enabled) { ItemsEnabledFlag = enabled; }
    public string Library => "ExampleService.dll";
}
