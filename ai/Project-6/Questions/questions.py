import os, fnmatch
import nltk
import sys
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1

nltk.download("punkt", quiet = True)
nltk.download("stopwords", quiet = True)

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
    d = {}
    txt_dir = os.path.join(os.getcwd(), directory)
    for file in os.listdir(txt_dir):
        if fnmatch.fnmatch(file, "*.txt"):
            with open(os.path.join(txt_dir, file), "r", encoding = "utf8") as txt_f:
                d[file] = txt_f.read()
    return d


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    return list(filter(lambda w: w not in stopwords.words('english') and not all(c in punctuation for c in w), map(lambda w: w.lower() ,word_tokenize(document))))


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    d = {}
    total_count = len(documents)
    for file_name in documents:
        for word in documents[file_name]:
            if word not in d:
                actual_count = sum(1 for fn in documents if word in documents[fn])
                d[word] = math.log(total_count / actual_count)
    return d


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    d = {}
    for file_name in files:
        d[file_name] = sum(files[file_name].count(word) * idfs[word] for word in query if word in files[file_name])
    return [k for k, _ in sorted(d.items(), key=lambda x: x[1], reverse=True)][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    d = {}
    for sentence, s_words in sentences.items():
        s_idf = 0
        qtc = 0
        for word in query:
            if word in s_words:
                s_idf += idfs[word]
                qtc += 1
        d[sentence] = (s_idf, qtc / len(sentence))
    sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=True)
    return [k for k, _ in sorted_d][:n]


if __name__ == "__main__":
    main()
