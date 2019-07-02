# 给定上限，查找小于它的质数，输出到result.txt中

function Find_Prime_Numbers([integer] $MAXLIMIT)
{
foreach $num in 2..$MAXLIMIT
[integer]$sqrt = $num.sqrt

