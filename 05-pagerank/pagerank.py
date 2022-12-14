import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    result = {}

    if len(corpus[page]) > 0:
        weight = damping_factor / len(corpus[page])
        residue = (1 - damping_factor) / (len(corpus.keys()) - len(corpus[page]))
    else:
        weight = damping_factor / len(corpus.keys())
        residue = weight

    for current_page in corpus.keys():
        if current_page in corpus[page]:
            result[current_page] = weight
        else:
            result[current_page] = residue

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_range = {}
    for current_page in corpus.keys():
        page_range[current_page] = 0

    page = random.choice(list(corpus.keys()))

    for _ in range(n):
        distribution = transition_model(corpus, page, damping_factor)
        random_value = random.random()
        count = 0
        for current_page in corpus.keys():
            count += distribution[current_page]
            if random_value <= count:
                page = current_page
                break
        page_range[page] += 1

    max_value = 0
    for current_page in corpus.keys():
        max_value += page_range[current_page]

    for current_page in corpus.keys():
        page_range[current_page] = page_range[current_page] / max_value

    return page_range


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_range = {}
    for current_page in corpus.keys():
        page_range[current_page] = 1 / len( corpus.keys() )

    base = (1 - damping_factor) / len(corpus.keys())

    for current_page in corpus.keys():
        aux_sum = 0
        for page in corpus.keys():
            if len(corpus[page]) == 0:
                aux_sum += page_range[page] / len(corpus.keys())
            elif current_page in corpus[page]:
                aux_sum += page_range[page] / len(corpus[page])

        page_range[current_page] = base + (damping_factor * aux_sum)

    max_value = 0
    for current_page in corpus.keys():
        max_value += page_range[current_page]

    for current_page in corpus.keys():
        page_range[current_page] = page_range[current_page] / max_value

    return page_range


if __name__ == "__main__":
    main()
