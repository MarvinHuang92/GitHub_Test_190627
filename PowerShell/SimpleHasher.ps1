function Hash($textToHash)

{
$hasher = new-object System.Security.Cryptography.SHA1Managed
$toHash = [System.Text.Encoding]::UTF8.GetBytes($textToHash)
$hashByteArray = $hasher.ComputeHash($toHash)



foreach($byte in $hashByteArray)
{$res += $byte #.ToString()
}

return $res;
}

$s = Hash("123457312331233451131254321")
write-host $s