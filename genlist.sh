cd $1
rm  list-raw
rm list
while read line ;do ./create $line 2>> list-raw 1>/dev/null; done < rip
awk 'BEGIN { FS = ": " }  ; { print $2 }' list-raw  | sed 's/ //g' >> list
