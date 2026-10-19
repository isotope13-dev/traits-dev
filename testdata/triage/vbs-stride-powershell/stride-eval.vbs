source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "This is ordinary generated output text."
source = source + "@(10,20,30,40,50,60)"
Set host = CreateObject("WScript.Shell")
Function Restore(value)
  index = 11
  width = 1
  result = ""
  While index <= Len(value) - 12
    result = result & Mid(value, index, width)
    index = index + 5
  Wend
  Restore = result
End Function
Execute source
