python ExtractAllWords.py ../dataset/OCCI/*.csv > ../results/OCCI_all_words.csv
python CountWords.py ../results/OCCI_all_words.csv | sort --reverse --key=2 --field-separator=, --numeric-sort > ../results/OCCI_word_counters.csv
