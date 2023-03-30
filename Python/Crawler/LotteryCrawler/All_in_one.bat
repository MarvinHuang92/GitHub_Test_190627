call fix_cache.bat<nul
sleep 3

pushd jiangsu\
start "" main.bat
popd

pushd national\
start "" main.bat
popd

sleep 3

exit
