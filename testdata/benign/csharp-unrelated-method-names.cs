class PresentationLabels
{
    private static string Combine(string first, string second) => first + second;
    private static string GetDirectoryName(string label) => label;

    public static string Caption()
    {
        return Combine("Combine", GetDirectoryName("GetDirectoryName"));
    }
}
