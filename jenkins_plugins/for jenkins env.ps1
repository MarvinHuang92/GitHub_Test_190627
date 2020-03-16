Write-Host $env:path

$env:JAVA_HOME = "xxxxxxxx\"
# Append a path
# $env:path = $env:path + ";" + $env:JAVA_HOME + "bin\"
# Overwrite all paths
$env:path = $env:JAVA_HOME + "bin\;C:\WINDOWS\System32\WindowsPowerShell\v1.0\"
$CLASSPATH = ".\"

# Call cmake_gen.bat
# .\1.bat


Write-Host "end of Powershell program"