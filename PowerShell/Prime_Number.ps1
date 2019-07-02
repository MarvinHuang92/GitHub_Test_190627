# 给定上限，查找小于它的质数，输出到result.txt中

function check_Prime_Number([int] $num_to_check)
{
# 检查输入值是否大于2
if ($num_to_check -lt 2){return $false}

[bool]$prime = $true
[int]$sqrt_root = [math]::Sqrt($num_to_check)
foreach ($num_to_devide in 2..$sqrt_root){
	$mod = $num_to_check % $num_to_devide
	if ($mod -eq 0){
		$prime = $false
		break
		}
	}
return $prime
}

$MAXLIMIT = 500
set-content -path .\result.txt -value ""
foreach ($i in 2..$MAXLIMIT){
$tag = $(& check_Prime_Number($i))
if ($tag -eq $true){
	add-content -path .\result.txt -value "$i"
	}
}
