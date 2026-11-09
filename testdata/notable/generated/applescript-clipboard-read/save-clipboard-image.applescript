property wanted : {{«class PNGf», ".png"}}

on run argv
	set outPath to (item 1 of argv)
	repeat with kind in wanted
		repeat with entry in (clipboard info)
			if (first item of entry) is equal to (first item of kind) then
				set fh to (open for access outPath with write permission)
				set eof fh to 0
				write (the clipboard as (first item of kind)) to fh
				close access fh
				return outPath
			end if
		end repeat
	end repeat
	return ""
end run
