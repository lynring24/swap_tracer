sudo mkdir -p tinted

for fname in `find $pwd -maxdepth 1 \( -name '*.c' -o -name '*.h' -o -name '*.cpp' \) -print` ; 
do 
	echo "brew ... " $fname
	$SWPTRACE/tint < $fname > ./tinted/$fname
done

