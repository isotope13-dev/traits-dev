package example
import r "reflect"
func describe(x any) { r.TypeOf(x); r.ValueOf(x); r.VisibleFields(r.TypeOf(x)) }
