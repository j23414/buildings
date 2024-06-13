
# Test case 1: Merge two TSV files with default options
$ python ../buildings/uniq_merge.py --cache one.tsv --new two.tsv
$ cat merged_cache_new.tsv
strain	date	clade	geo	age	patient	col_date	group
A	2022-01-01	alpha	iowa	-N/A-			
B	2022-02-02	beta,beta2	washington	-N/A-	marley		
C	2022-03-03	gamma	,	-N/A-	rick		
D		delta		,	bob		

# Test case 2: Merge two TSV files with custom delimiters
$ python ../buildings/uniq_merge.py --cache one.tsv --new two.tsv --cache_delim="\t" --new_delim="\t" --outfile_delim=","
$ cat merged_cache_new.tsv
strain,date,clade,geo,age,patient,col_date,group
A,2022-01-01,alpha,iowa,-N/A-,,,
B,2022-02-02,beta,beta2,washington,-N/A-,marley,,
C,2022-03-03,gamma,,,-N/A-,rick,,
D,,delta,,,bob,,

# Test case 3: Merge two TSV files with conflict resolution set to 'left'
$ python ../buildings/uniq_merge.py --cache one.tsv --new two.tsv --conflict_resolution=left
$ cat merged_cache_new.tsv
strain	date	clade	geo	age	patient	col_date	group
A	2022-01-01	alpha	iowa	-N/A-			
B	2022-02-02	beta	washington	-N/A-	marley		
C	2022-03-03	gamma		-N/A-	rick		
D		delta		,	bob		

# Test case 4: Merge two TSV files with conflict resolution set to 'right'
$ python ../buildings/uniq_merge.py --cache one.tsv --new two.tsv --conflict_resolution=right
$ cat merged_cache_new.tsv
strain	date	clade	geo	age	patient	col_date	group
A	2022-01-01	alpha	iowa	-N/A-			
B	2022-02-02	beta2	washington	-N/A-	marley		
C	2022-03-03	gamma		-N/A-	rick		
D		delta		,	bob		
