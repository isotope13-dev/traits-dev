Import-Module Pester

# Sequential 1..N matrix contents are test data, not char codes: decoded as
# text they are control characters. Neither numeric-array atom may fire here.
Describe "Matrix-Lookup" {
    It "Should navigate a 3d matrix" {
        $dimensions = @(2, 2, 2)
        $matrix = @(
           1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        )
        GetNdMatrixElement @(0, 0, 0) $matrix $dimensions | Should -Be 1
    }
}
