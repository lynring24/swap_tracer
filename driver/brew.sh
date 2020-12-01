sudo mkdir -p modified

for fname in `find $pwd -maxdepth 1 \( -name '*.c' -o -name '*.h' -o -name '*.cpp' \) -print` ; 
do 
	echo $fname
	$SWPTRACE/brew < $fname > ./modified/$fname
done

