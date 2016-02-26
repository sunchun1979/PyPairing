param(
	[string]$inp,
	[string]$res,
	[string]$out,
	$round
)

python .\Pair.py -r $round -i $inp -o $res
Import-Csv $res | ConvertTo-Html | Out-File _pairing.html
Invoke-Item _pairing.html
Invoke-Expression ("Notepad " + $res)
