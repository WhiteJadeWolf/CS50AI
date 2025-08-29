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

    N = len(corpus) # total no. of webpages in the corpus
    if not corpus[page]:
        return dict.fromkeys(list(corpus.keys()), (1 / N))
    numlink = len(corpus[page]) # total no. of links to other webpages in the current webpage
    page_pd = {p : ((1 - damping_factor) / N) for p in corpus}
    for linkedpage in corpus[page]:
        page_pd[linkedpage] += damping_factor / numlink
    return page_pd
        

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pagerank = dict.fromkeys(list(corpus.keys()), 0)
    sample = random.choice(list(corpus.keys()))
    pagerank[sample] += 1 / n
    for i in range(1,n):
        page_pd = transition_model(corpus, sample, damping_factor)
        pages = list(page_pd.keys())
        probs = list(page_pd.values())
        sample = random.choices(pages, probs, k=1)[0]
        pagerank[sample] += 1 / n
    return pagerank
        

def exit_condition(pagerank, newrank, tolerance = 0.001):
    return (max(abs(newrank[p] - pagerank[p]) for p in newrank) <= tolerance)
    
    
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    pagerank = dict.fromkeys(list(corpus.keys()), (1 / N))
    
    for page in corpus:
        if len(corpus[page]) == 0:
            corpus[page] = set(corpus.keys())
            
    while True:
        newrank = {}
        for p in corpus:
            newrank[p] = (1 - damping_factor) / N
            for i in corpus:
                if p in corpus[i]:
                    newrank[p] += damping_factor * (pagerank[i] / len(corpus[i]))
        if exit_condition(pagerank, newrank):
            break
        else:
            pagerank = newrank.copy()
    return newrank


if __name__ == "__main__":
    main()