param(
	[string]$inp,
	[string]$res,
	[string]$out
)
python .\Standing.py -i $inp -r $res -o $out
Import-Csv $out | ConvertTo-Html | Out-File _standing.html
Invoke-Item _standing.html
