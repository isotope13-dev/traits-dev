module example.invalid/application
go 1.25
require example.invalid/library v1.0.0
replace example.invalid/library => ../local-library
