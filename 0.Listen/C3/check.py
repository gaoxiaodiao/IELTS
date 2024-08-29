#!/usr/bin/env python
import sys
import json
import os

def load_correct_words(filename):
    names = []
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            if 'name' in item:
                names.append(item['name'].lower())
    return names, data

def load_transcribed_words(filename):
    transcribed_words = []
    with open(filename, 'r') as file:
        for line in file:
            words = [word.strip().lower() for word in line.split(',') if word.strip()]
            transcribed_words.extend(words)
    return transcribed_words

def check_words(correct_words, transcribed_words):
    incorrect_words = []
    results = []
    correct_count = 0
    incorrect_count = 0
    for i, correct_word in enumerate(correct_words):
        try:
            trans_word = transcribed_words[i]
            if correct_word == trans_word:
                results.append(f"{correct_word} ✅")
                correct_count += 1
            else:
                results.append(f"{correct_word} ❌ ({trans_word})")
                incorrect_words.append(correct_word)
                incorrect_count += 1
        except IndexError:
            results.append(f"{correct_word} ❌ (missing)")
            incorrect_words.append(correct_word)
            incorrect_count += 1
    return results, incorrect_words, correct_count, incorrect_count

def update_incorrect_words_json(incorrect_words, all_words_data):
    filename = 'incorrect_words.json'
    existing_data = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    
    existing_names = set(item['name'].lower() for item in existing_data)
    
    for word in incorrect_words:
        word_data = next((item for item in all_words_data if item['name'].lower() == word), None)
        if word_data and word.lower() not in existing_names:
            existing_data.append(word_data)
            existing_names.add(word.lower())
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=2)

def main():
    if len(sys.argv) != 3:
        print("Usage: python check.py <correct_file> <transcribed_file>")
        sys.exit(1)
    
    correct_file, transcribed_file = sys.argv[1], sys.argv[2]
    correct_words, all_words_data = load_correct_words(correct_file)
    transcribed_words = load_transcribed_words(transcribed_file)
    results, incorrect_words, correct_count, incorrect_count = check_words(correct_words, transcribed_words)
    
    for result in results:
        print(result)
    
    print(f"\nCorrect words: {correct_count}, Incorrect words: {incorrect_count}")
    update_incorrect_words_json(incorrect_words, all_words_data)
    print("Incorrect words have been updated in incorrect_words.json")

if __name__ == '__main__':
    main()