# Bigram

We have a looong book (600 KB, about the size of Moby Dick), encrypted with bialphabetic substitution (like monoalphabetic, but with pairs of letters).
Fortunately, spaces and other special characters are kept, as well as whether capital/small letter.
For leftover letters (odd-length words), we have an additional monoalphabetic substitution.

Solution via:
* Frequency analysis
* sharp looking at the partially decoded text
* use a complete list of english words and `grep`

Wikipedia has a list of letter frequencies and frequencies of 39 bigrams and the most common english words.
* 39 is not enough
* their freq. is given in an unsatisfying way
* their freq. don't differ enough for automated substitution
* letter freq. are different between general and last letter of word
* There are other freq. we want to exploit.

So I decided to compute my own frequencies, based on some free texts
* Moby Dick
* Alice in Wonderland
* Gulliver's Travels
* 3 Little Pigs
* King John
* Love's Labour's Lost

These freq. included:
* letter pairs
* single letters at word's end
* word beginnings
* full words

Then encryption can be done by
* The flag formaty `cybrics` gives 3 pairs and 1 letter
* The word `the` is by far the most common: 1 pair, 1 letter
* word of single capital letter: `I` 1 letter
* use the next few most common pairs: in, to, an
* iterate
  * apply known mapping
  * looks for word with few gaps
  * guess the word, grep in wordlist to make sure, it is unique (or alternatives don't make sense)
  * obtain new mappings

In the end, this took about 6 hours, but looking back, I could have automated more and made more use of case sensitivity.
