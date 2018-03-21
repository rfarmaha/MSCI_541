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

 The term frequency of document is represented in BM-25 via the component: `[(k_1 + 1)f_i]/(K + f_i)`. The `f_i` term is
 the frequency of term i in the document, while `k_1` is a  constant. `K = k_1[(1 - b) +b * dl/avdl]`, where `b` is 
 another constant, `dl` and `avdl` are the document length and average document length of all documents respectively.
 Thus, the term frequency, represented in the numerator, is normalized by the length of the document (the `K` variable)
 in the denominator. This achieves a similar effect to computing the logarithm of the term frequency in the document,
 which is used in the tf-idf calculation.
 
 ### Problem 3
 
 Stemming would speed up the retrieval speed, as there would be fewer terms indexed, producing a much thinner vocabulary.
 For example, the words: "fish", "fishes", "fishing" would all be stemmed to "fish", thus reducing the number of words 
 that involve fish from 3 to 1 in the vocabulary. When a query for "fishes" appears, its stem (i.e. "fish") would be
 retrieved from the vocabulary.
 
 ### Problem 4