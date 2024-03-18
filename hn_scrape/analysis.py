import csv
from collections import Counter
import re

def clean_word(word):
    return re.sub(r'\W+', '', word).lower()

def count_words_in_column(filename, column_name):
    word_count = Counter()
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            # Split the column content into words, clean them, and count occurrences
            words = row[column_name].split()
            cleaned_words = [clean_word(word) for word in words]
            word_count.update(cleaned_words)
    return word_count

def print_top_words(counter, top_n=10):
    for word, count in counter.most_common(top_n):
        print(f'{word}: {count}')

filename = '1000_output_deduplicated.csv'

for column in ['location', 'remote', 'relocate', 'technologies']:
    print(f"Top 10 most common words in {column}:")
    counter = count_words_in_column(filename, column)
    print_top_words(counter)
    print("---\n")
