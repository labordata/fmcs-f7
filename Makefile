.PHONY : all
all : 
	$(MAKE) update_raw
	$(MAKE) f7.csv f7.db

f7.db : f7.csv link.csv
	csvs-to-sqlite $^ $@

no_exact_unions.csv : f7.csv
	csvcut -c union_name,union_city,union_state $< | \
            python scripts/normalize.py | \
            csvsort | \
            uniq > $@

link_units.csv : no_exact_unions.csv opdr_local.csv
	python scripts/link_locals.py $^ $@ -v -v

f7.csv : $(patsubst %.xlsx,%.csv,$(wildcard raw/*.xlsx))
	python scripts/to_csv.py $^ | \
            csvsort | \
            uniq | \
            csvcut -x -l | \
            sed '1s/line_number/id/' > $@

opdr_local_0.csv :
	wget -O $@ "https://labordata.bunkum.us/opdr-142d1ae.csv?sql=with+most_recent_lu+as+(%0D%0A++select%0D%0A++++*%0D%0A++from%0D%0A++++(%0D%0A++++++select%0D%0A++++++++*%0D%0A++++++from%0D%0A++++++++lm_data%0D%0A++++++order+by%0D%0A++++++++f_num%2C%0D%0A++++++++receive_date+desc%0D%0A++++)+t%0D%0A++group+by%0D%0A++++f_num%0D%0A)%0D%0Aselect%0D%0A++aff_abbr+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+abbr_local_name%2C%0D%0A++coalesce(%0D%0A++++regexp_match(%27(.*%3F)(%2C%3F+AFL-CIO%24)%27%2C+union_name)%2C%0D%0A++++regexp_match(%27(.*%3F)(+IND%24)%27%2C+union_name)%2C%0D%0A++++union_name%0D%0A++)+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+full_local_name%2C%0D%0A++*%0D%0Afrom%0D%0A++most_recent_lu%0D%0Awhere%0D%0A++desig_name+IN+('LU', 'LG', 'LDIV')++and+desig_num+is+not+null+limit+5000+offset+0&_size=max"

opdr_local_1.csv :
	wget -O $@ "https://labordata.bunkum.us/opdr-142d1ae.csv?sql=with+most_recent_lu+as+(%0D%0A++select%0D%0A++++*%0D%0A++from%0D%0A++++(%0D%0A++++++select%0D%0A++++++++*%0D%0A++++++from%0D%0A++++++++lm_data%0D%0A++++++order+by%0D%0A++++++++f_num%2C%0D%0A++++++++receive_date+desc%0D%0A++++)+t%0D%0A++group+by%0D%0A++++f_num%0D%0A)%0D%0Aselect%0D%0A++aff_abbr+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+abbr_local_name%2C%0D%0A++coalesce(%0D%0A++++regexp_match(%27(.*%3F)(%2C%3F+AFL-CIO%24)%27%2C+union_name)%2C%0D%0A++++regexp_match(%27(.*%3F)(+IND%24)%27%2C+union_name)%2C%0D%0A++++union_name%0D%0A++)+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+full_local_name%2C%0D%0A++*%0D%0Afrom%0D%0A++most_recent_lu%0D%0Awhere%0D%0A++desig_name+IN+('LU', 'LG', 'LDIV')++and+desig_num+is+not+null+limit+5000+offset+5001&_size=max"

opdr_local_2.csv :
	wget -O $@ "https://labordata.bunkum.us/opdr-142d1ae.csv?sql=with+most_recent_lu+as+(%0D%0A++select%0D%0A++++*%0D%0A++from%0D%0A++++(%0D%0A++++++select%0D%0A++++++++*%0D%0A++++++from%0D%0A++++++++lm_data%0D%0A++++++order+by%0D%0A++++++++f_num%2C%0D%0A++++++++receive_date+desc%0D%0A++++)+t%0D%0A++group+by%0D%0A++++f_num%0D%0A)%0D%0Aselect%0D%0A++aff_abbr+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+abbr_local_name%2C%0D%0A++coalesce(%0D%0A++++regexp_match(%27(.*%3F)(%2C%3F+AFL-CIO%24)%27%2C+union_name)%2C%0D%0A++++regexp_match(%27(.*%3F)(+IND%24)%27%2C+union_name)%2C%0D%0A++++union_name%0D%0A++)+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+full_local_name%2C%0D%0A++*%0D%0Afrom%0D%0A++most_recent_lu%0D%0Awhere%0D%0A++desig_name+IN+('LU', 'LG', 'LDIV')++and+desig_num+is+not+null+limit+5000+offset+10001&_size=max"

opdr_local_3.csv :
	wget -O $@ "https://labordata.bunkum.us/opdr-142d1ae.csv?sql=with+most_recent_lu+as+(%0D%0A++select%0D%0A++++*%0D%0A++from%0D%0A++++(%0D%0A++++++select%0D%0A++++++++*%0D%0A++++++from%0D%0A++++++++lm_data%0D%0A++++++order+by%0D%0A++++++++f_num%2C%0D%0A++++++++receive_date+desc%0D%0A++++)+t%0D%0A++group+by%0D%0A++++f_num%0D%0A)%0D%0Aselect%0D%0A++aff_abbr+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+abbr_local_name%2C%0D%0A++coalesce(%0D%0A++++regexp_match(%27(.*%3F)(%2C%3F+AFL-CIO%24)%27%2C+union_name)%2C%0D%0A++++regexp_match(%27(.*%3F)(+IND%24)%27%2C+union_name)%2C%0D%0A++++union_name%0D%0A++)+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+full_local_name%2C%0D%0A++*%0D%0Afrom%0D%0A++most_recent_lu%0D%0Awhere%0D%0A++desig_name+IN+('LU', 'LG', 'LDIV')++and+desig_num+is+not+null+limit+5000+offset+15001&_size=max"

opdr_local_4.csv :
	wget -O $@ "https://labordata.bunkum.us/opdr-142d1ae.csv?sql=with+most_recent_lu+as+(%0D%0A++select%0D%0A++++*%0D%0A++from%0D%0A++++(%0D%0A++++++select%0D%0A++++++++*%0D%0A++++++from%0D%0A++++++++lm_data%0D%0A++++++order+by%0D%0A++++++++f_num%2C%0D%0A++++++++receive_date+desc%0D%0A++++)+t%0D%0A++group+by%0D%0A++++f_num%0D%0A)%0D%0Aselect%0D%0A++aff_abbr+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+abbr_local_name%2C%0D%0A++coalesce(%0D%0A++++regexp_match(%27(.*%3F)(%2C%3F+AFL-CIO%24)%27%2C+union_name)%2C%0D%0A++++regexp_match(%27(.*%3F)(+IND%24)%27%2C+union_name)%2C%0D%0A++++union_name%0D%0A++)+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+full_local_name%2C%0D%0A++*%0D%0Afrom%0D%0A++most_recent_lu%0D%0Awhere%0D%0A++desig_name+IN+('LU', 'LG', 'LDIV')++and+desig_num+is+not+null+limit+5000+offset+20001&_size=max"

opdr_local_5.csv :
	wget -O $@ "https://labordata.bunkum.us/opdr-142d1ae.csv?sql=with+most_recent_lu+as+(%0D%0A++select%0D%0A++++*%0D%0A++from%0D%0A++++(%0D%0A++++++select%0D%0A++++++++*%0D%0A++++++from%0D%0A++++++++lm_data%0D%0A++++++order+by%0D%0A++++++++f_num%2C%0D%0A++++++++receive_date+desc%0D%0A++++)+t%0D%0A++group+by%0D%0A++++f_num%0D%0A)%0D%0Aselect%0D%0A++aff_abbr+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+abbr_local_name%2C%0D%0A++coalesce(%0D%0A++++regexp_match(%27(.*%3F)(%2C%3F+AFL-CIO%24)%27%2C+union_name)%2C%0D%0A++++regexp_match(%27(.*%3F)(+IND%24)%27%2C+union_name)%2C%0D%0A++++union_name%0D%0A++)+%7C%7C+%27+local+%27+%7C%7C+desig_num+as+full_local_name%2C%0D%0A++*%0D%0Afrom%0D%0A++most_recent_lu%0D%0Awhere%0D%0A++desig_name+IN+('LU', 'LG', 'LDIV')+++and+desig_num+is+not+null+limit+5000+offset+25001&_size=max"


opdr_local.csv : opdr_local_0.csv opdr_local_1.csv opdr_local_2.csv opdr_local_3.csv opdr_local_4.csv opdr_local_5.csv
	csvstack $^ > $@




%.csv : %.xlsx
	in2csv $< | sed '/^Notice Date/,$$!d' > $@

.PHONY : update_raw
update_raw :
	curl -k https://www.fmcs.gov/resources/documents-and-data/#tab-d3d7f5344cef9bab4d3 | grep Notices.xlsx | sed -n 's/.*href="\([^"]*\).*/\1/p' | wget --no-check-certificate -nd -i - -P raw -nc
