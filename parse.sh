now=$(date '+%Y%m%d')
cd $now
rm alldata.xml
for filename in *.hex; do ../mbus_parse_hex $filename >> alldata.xml ;echo $filename ; done
