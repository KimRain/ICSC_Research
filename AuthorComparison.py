#find all identical authors (maybe also find all authors that are slightly different)
#compare the co-authors of all identical authors
#if co-authors don't coincide then authors are likely different people

import pandas as pd
from ast import literal_eval
from collections import defaultdict

#temporary author dict here, would get actual dict from fakepubs.py
Authors = {'UDAXIHHEXD': 1, 'ACGHQTARGW': 1, 'SIZAYZFWNK': 1, 'YKDCMDLLTI': 1, 'RDMCRJUTLS': 1, 'YJCHDMIOUL': 1,
           'VIWVUCTUFR': 1, 'MIUWRHVKYY': 1, 'ZKMICGSWKG': 2, 'UOEIEHXRRI': 1, 'VPRFIQTNGR': 1, 'HSHACWUBHC': 1,
           'CQHIVPGREX': 1, 'ZNGDDVNLNN': 1, 'UDBMXKZDHG': 1, 'IOHCOZRDBU': 1, 'YHFNPPGMBF': 1, 'IZZOJNWXZR': 1,
           'GBSXRBXKBB': 1, 'VDEIDDXREI': 1, 'IQPIBCUNIB': 1, 'UIFXORWNRA': 1, 'WERBLSRENE': 1, 'ZBLGVHVDLY': 1,
           'XEHFZZFNAF': 1, 'XZHIFZWDMB': 1, 'OLJZHHAVGM': 1, 'YILUQMVRKA': 1, 'IBDTNLXZKN': 1}

def find_freq_authors(author_dict):
    authors_with_same_name = []
    for author, count in Authors.items():
        if count > 1:
            authors_with_same_name.append(author)
    print(authors_with_same_name)
    return authors_with_same_name

#find all the pubs this author is involved in from authors only .csv

def process_authors_csv(filename, author_names):
    pd.set_option('display.max_colwidth', None)
    df = pd.read_csv(filename)
    df['Authors'] = df['Authors'].apply(lambda x: literal_eval(x))

    # Filter publications where any of the frequent authors appear
    publications_with_frequent_authors = df[
        df['Authors'].apply(lambda authors: any(author in author_names for author in authors))]

    print("Publications with authors who appear more than once:")
    print(publications_with_frequent_authors)
    return df

#now we need to make an adjacency matrix for each author
#create multiple occurrences for each author with the same name


def process_authors_csv(filename, author_names):
    pd.set_option('display.max_colwidth', None)
    df = pd.read_csv(filename)
    df['Authors'] = df['Authors'].apply(lambda x: literal_eval(x))  # Convert string to list

    # Filter publications where any of the frequent authors appear
    publications_with_frequent_authors = df[
        df['Authors'].apply(lambda authors: any(author in author_names for author in authors))
    ]

    print("Publications with authors who appear more than once:")
    print(publications_with_frequent_authors)
    return publications_with_frequent_authors


def get_co_authors(df, author_name):
    co_authors_dict = defaultdict(list)
    occurrence = 1

    for authors in df['Authors']:
        if author_name in authors:
            co_authors = [author for author in authors if author != author_name]
            co_authors_dict[occurrence].extend(co_authors)
            occurrence += 1

    return co_authors_dict

def compare_co_authors(co_authors_dict, author_name):
    occurrences = list(co_authors_dict.keys())

    if len(occurrences) < 2:
        print(f"Not enough occurrences of {author_name} to compare.")
        return

    for i in range(len(occurrences)):
        for j in range(i + 1, len(occurrences)):
            co_authors_1 = set(co_authors_dict[occurrences[i]])
            co_authors_2 = set(co_authors_dict[occurrences[j]])

            print(f"Comparing co-authors of occurrence {occurrences[i]} and {occurrences[j]} of {author_name}:")
            print(f"Co-authors of occurrence {occurrences[i]}: {co_authors_1}")
            print(f"Co-authors of occurrence {occurrences[j]}: {co_authors_2}")

            common_co_authors = co_authors_1.intersection(co_authors_2)
            if common_co_authors:
                print(f"Common co-authors between occurrence {occurrences[i]} and {occurrences[j]} of {author_name}: {common_co_authors}")
                print(f"These occurrences are likely the same individual.")
            else:
                print(f"No common co-authors between occurrence {occurrences[i]} and {occurrences[j]} of {author_name}.")
                print(f"These occurrences are likely different individuals.")

    print("\n")


#calling fxns
authors_with_same_name = find_freq_authors(Authors)
df = process_authors_csv('authors_only.csv', authors_with_same_name)
co_authors_dict = get_co_authors(df, authors_with_same_name)

for frequent_author in authors_with_same_name:
    co_authors_dict = get_co_authors(df, frequent_author)
    compare_co_authors(co_authors_dict, frequent_author)

'''
from here we would get rid the duplicates in the full authors list,
which will likely be indexed and remove the authors that are likely 
the same person then assign porcids.

We also need to find a way to evaluate the intersection
method above. 

"How do we score how well we did at solving the unique vs. redundant names?"

K-means clustering? using our unlabeled data? then we can compare results...

'''
