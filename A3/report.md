# MSCI 541 HW3 Report
Ramandeep Farmaha 20516974

## Problem 1

Using precision at rank 10 is more beneficial than using average precision in the cases where there is a significantly
large number of relevant documents for a query, and the user only cares about the first page of results. An example would be
a textbook database: a query such as "Microeconomics: Tenth Edition" would return potentially hundreds of results, with only the top books being relevant to the user. 
In this case, it's better to use precision at rank 10 as an evaluation metric because the user only cares about the top results
and is unlikely to browse the next pages. If A is an information retrieval system that has a higher precision rank at 10
but lower average precision than system B for a particular query, it is more beneficial for the user to use system A, because
she will only look at the first page of results, which are more relevant from system A. 

## Problem 2


**Advantage 1**: NDCG is much more fine tuned than precision rank at 10. For example, if there are two retrieval systems
A and B, which rank the top ten documents for a given query as: {1, 0, 1, 1, 1, 0, 0, 1, 0, 1} and {1, 1, 0, 1, 1, 1, 1, 0, 0, 0}
respectively, the precision ranks at 10 for both systems are identical, as they both contain 6 relevant documents in the top ten results.
However, system B will have a higher NDCG than system A because its relevant results are clustered at the top of the list, making it
a better option than system A. Web search engines would prefer to use NDCG, as it promotes models where the most relevant documents
are clustered to the top.

**Advantage 2**: Precision rank at 10 assumes a binary representation of relevance: either the document is relevant or it isn't.
NDCG, on the other hand, assigns a relevance score that varies in levels (perfect, excellent, good, fair, bad), which allows for 
a higher resolution of decision making. This is beneficial for a web search engine where a user may wish to access webpages that
are tangentially related to their query (i.e. if a user queries for "Cairo" and a document pertaining to "Giza" is returned).

## Problem 3

### Part A
