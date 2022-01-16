# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 11:07:08 2022

@author: chris
"""
from typing import Set
from nltk.corpus import brown

def load_five_char_eng_words(char_set: str) -> Set[str]:
    word_list = []
    for word in brown.words():
        if len(word) == 5:
            add = True
            for letter in word:
                if letter not in char_set:
                    add = False
            
            if add:
                word_list.append(word.lower())
    return set(word_list)

def export_five_cha_eng_words(word_list: Set[str], filename: str) -> None:
    export = [word+'\n' for word in five_cha_eng_words]
    with open(filename, 'w') as file:
        # for item in word_list:
        #     file.write(item + '\n')
        file.writelines(export)

if __name__ == "__main__":
    characters = "abcdefghijklmnopqrstuvwxyz"
    five_cha_eng_words = load_five_char_eng_words(characters)
    export_five_cha_eng_words(five_cha_eng_words, 'dict_file.txt')