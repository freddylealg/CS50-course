import math
import string

import nltk
import sys
import os
from nltk.tokenize import word_tokenize

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = {}
    file_list = os.listdir(directory)
    for file in file_list:
        f = open(directory + os.sep + file, "r", encoding="utf-8")
        data[file] = f.read()
    return data


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenize = word_tokenize( document )

    for puntuation in string.punctuation:
        tokenize = list(filter(lambda a: a != puntuation, tokenize))
    tokenize = list(filter(lambda a: a != '``', tokenize))
    tokenize = list(filter(lambda a: a != '""', tokenize))
    tokenize = list(filter(lambda a: a != '\'\'', tokenize))


    for stopword in nltk.corpus.stopwords.words("english"):
        tokenize = list(filter(lambda a: a != stopword, tokenize))

    tokenize = [word.lower() for word in tokenize]
    return tokenize


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    data = {}
    count_corpus = len( documents )
    for document in documents:
        for word in documents[document]:
            if word in data:
                data[word] += 1
            else:
                data[word] = 1

    for word in data.keys():
        data[word] = math.log(count_corpus / (float(data[word])) )

    return data


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    data = {}
    for file in files:
        data[file] = 0

    for word in query:
        if word in idfs:
            for file in files:
                tf = files[file].count(word)
                data[file] += tf * idfs[word]

    data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}
    data_sort = list(data.keys())
    return data_sort[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    data = {}
    for sentence in sentences:
        data[sentence] = 0

    for sentence in sentences:
        for word in query:
            if word in sentences[sentence]:
                data[sentence] += idfs[word]

    data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}
    data_sort = list(data.keys())[::-1]
    return data_sort[:n]


if __name__ == "__main__":
    main()
