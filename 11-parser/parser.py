import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# Original nonterminals
# NONTERMINALS = """
# S -> NP | NP V | NP V NP | NP V S | NP V NP Conj S | NP V NP Conj V S | NP V Adv Conj V S
# NP -> N | N Conj | N Conj N | N Adj | N Adv | N P | N P NP
# NP -> P N | P Det N | P Det N Adv | P Det Adj NP
# NP -> Det N | Det N Adv | Det N NP | Det Adj | Det Adj NP | N
# NP -> Adj NP
# """

# Debug nonterminals
NONTERMINALS = """
S -> NP | V | NP V | NP V S | NP Conj S | Adv Conj V S
NP -> N | N Conj | N Conj N | N Adj | N Adv | N P | N P NP
NP -> P N | P Det N | P Det N Adv | P Det Adj NP 
NP -> Det N | Det N Adv | Det N NP | Det Adj | Det Adj NP | N
NP -> Adj NP  
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    print(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.replace(".", "").replace("\n", "").lower()
    sentence = sentence.strip()
    word_list = sentence.split(" ")
    return word_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    list_to_return = []
    count = 0
    for aux in tree:
        if aux.label() == 'NP':
            list_to_return.append( aux )
        elif aux.label() == 'S':
            list_to_return.extend( np_chunk( tree[count] ) )
        count += 1
    return list_to_return


if __name__ == "__main__":
    main()
