# MSCI 541 HW4 Report
Ramandeep Farmaha 20516974

## Problem 1

Two documents can have the same retrieval score and be relevant and non-relevant respectively if one of the documents
has a shorter length but less term frequency, while the other document has a much longer length and greater term
frequency, allowing both documents to have the same term frequency index. The shorter document could potentially be not
relevant, because it only shows the term once or twice, but because of its shorter length (i.e. perhaps 200 words), it 
could have the same term frequency index as a much longer document (i.e. 8000 words) that repeats the term 20 times.

### Problem 2

#### Part A

Long documents can have words that occur once and words (such as "the") appear hundreds of times. Although normalization
may stymie the effects of the more frequent terms, it is better to use the logarithm of the number of term occurrences.

### Part B

 The term frequency of document is represented in BM-25 via the component: \frac{n!}{k!(n -k)!}