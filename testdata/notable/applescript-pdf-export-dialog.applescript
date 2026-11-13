-- Positive fixture: a legitimate AppleScript PDF export dialog. The dialog
-- text names "the password for the PDF" as an export option, which the
-- PDF-export password-prompt trait must recognize (it suppresses the
-- generic phishing-lure composite for this benign export flow).
on exportDocument(docAlias, outputPath)
	set exportPassword to text returned of (display dialog "Enter the password for the PDF export" default answer "" buttons {"Cancel", "Export"} default button "Export" with title "Export PDF")
	tell application "Pages"
		export docAlias to POSIX file outputPath as PDF with properties {password:exportPassword}
	end tell
end exportDocument
