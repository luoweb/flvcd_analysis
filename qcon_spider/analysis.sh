grep "href=\"/slide/show.*\"" qcon_ppt.txt
grep -o "href=\"/slide/show.*\"" qcon_ppt.txt  | awk '{print $1}' | grep -o "/slide.*[0-9]"  > qcon_ppt_href.txt
grep -A 1 "/presentation/.*\"" qcon_title.html | grep h4 | grep -o ">.*<"  > qcon_title.txt
grep -o "/presentation/.*\"" qcon_title.html | awk -F '"' '{print "https://2018.qconshanghai.com"$1}'  > qcon_content_short.txt

cat qcon_content_short.txt| xargs -I TT -n 1 sh -c "python get_dyn_url.py TT"