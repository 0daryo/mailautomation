#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from glob import iglob
import re

import MeCab
import markovify


def load_from_file(files_pattern):
    """read and merge files which matches given file pattern, prepare for parsing and return it.
    """

    # read text
    file = open(files_pattern, "r")
    text = file.read()
    return text


def split_for_markovify(text):
    """split text to sentences by newline, and split sentence to words by space.
    """
    # separate words using mecab
    m = MeCab.Tagger("-chasen")
    splitted_text = ""

    # these chars might break markovify
    # https://github.com/jsvine/markovify/issues/84

    # split whole text to sentences by newline, and split sentence to words by space.
    for line in text.split():
        mp = m.parse(line)
        while mp:
            try:
                if mp.surface != '。' and mp.surface != '、':
                    splitted_text += ' '    # split words by space
                if mp.surface == '。':
                    splitted_text += '\n'    # reresent sentence by newline
            except UnicodeDecodeError as e:
                # sometimes error occurs
                print(line)
            finally:
                mp = mp.next

    return splitted_text


def main():
    # load text
    rampo_text = load_from_file('/Users/administrator/pythonWorkplace/mail_automation/test.text')

    # split text to learnable form
    splitted_text = split_for_markovify(rampo_text)

    # learn model from text.
    text_model = markovify.NewlineText(splitted_text, state_size=3)

    # ... and generate from model.
    sentence = text_model.make_sentence()
    print(''.join(sentence.split()))    # need to concatenate space-splitted text

    # save learned data
    with open('learned_data.json', 'w') as f:
        f.write(text_model.to_json())

    # later, if you want to reuse learned data...
    """
    with open('learned_data.json') as f:
        text_model = markovify.NewlineText.from_json(f.read())
    """


if __name__ == '__main__':
    main()