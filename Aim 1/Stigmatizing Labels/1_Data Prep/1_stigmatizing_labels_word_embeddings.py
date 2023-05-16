import numpy
import pandas as pd
import Cython
import gensim
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
from collections import defaultdict
from gensim.models import Word2Vec, KeyedVectors
import Levenshtein, re
import sys

#model = KeyedVectors.load_word2vec_format('trig-vectors-phrase.bin', binary=True, encoding='latin-1')
model2 = KeyedVectors.load_word2vec_format('trig-vectors-phrase.txt', binary=False)

# stigma OR bias OR stereotype OR abuser OR stereotype
# NIDA: https://www.drugabuse.gov/nidamed-medical-health-professionals/health-professions-education/words-matter-terms-to-use-avoid-when-talking-about-addiction
# Included: Addict, User, Abuser, Junkie, Alcoholic, Drunk, Habit, Dirty,
# Added in this study: stigma, bias, stereotype, shame, blame (From studies on stigma, bias, and types of stigmatization referenced in literature)
# Not included: clean, addicted baby, opioid substitution replacement therapy, medication-assisted treatment, former addict, reformed adict

bias_stem_words = ["addict","user","abuser","junkie","alcoholic", "drunk", "habit", "dirty", "stigma","bias","stereotype","shame","blame"]


bias_words_df = pd.DataFrame({
    'stem_word': bias_stem_words
})


bias_words_df['most_similar_words'] = bias_words_df['stem_word'].apply(model2.most_similar)

bias_words_df_2 = bias_words_df.explode("most_similar_words", ignore_index=True)
bias_words_df_2['new_word_id'] = range(1, 1 + len(bias_words_df_2))
# bias_words_df_2[['similar_word','similarity_score']] =
words_sep = pd.DataFrame(bias_words_df_2['most_similar_words'].values.tolist())
words_sep['new_word_id'] = range(1, 1 + len(bias_words_df_2))
bias_words_3 = bias_words_df_2.merge(words_sep, on = 'new_word_id')
#bias_words_3['similar_word'], bias_words_3['score'] = bias_words_3[3],bias_words_3[4]

bias_words_3= bias_words_3.rename(columns={0: "similar_word", 1: "score"})
bias_words_3["Relevant_to_study"] = ""
bias_words_3.to_csv("bias_lexicon_stem_and_similar_round1.csv")


## Misspelling Generator



def generate_spelling_variants(seedwordlist, word_vectors, semantic_search_length=500, levenshtein_threshold = 0.85, setting = 1):
    """
        setting -> 0 = weighted levenshtein ratios
                -> 1 = standard levenshtein ratios

    :param seedwordlist:            list of words for which spelling variants are to be generated
    :param word_vectors:            the word vector model
    :param semantic_search_length:  the number of semantically similar terms to include in each iteration
    :param levenshtein_threshold:   the threshold for levenshtein ratio

    :return: dictionary containing the seedwords as key and all the variants as a list of values

    """
    vars = defaultdict(list)
    for seedword in seedwordlist:
        #a dictionary to hold all the variants, key: the seedword, value: the list of possible misspellings
        #a dynamic list of terms that are still to be expanded
        terms_to_expand = []
        terms_to_expand.append(seedword)
        all_expanded_terms = []
        level = 1
        while len(terms_to_expand)>0:
                t = terms_to_expand.pop(0)
                all_expanded_terms.append(t)
                try:
                    similars = word_vectors.most_similar(t, topn=semantic_search_length)
                    for similar in similars:
                        similar_term = similar[0]
                        if setting == 1:
                            seq_score = Levenshtein.ratio(str(similar_term),seedword)
                        if setting == 0:
                            seq_score = weighted_levenshtein_ratio(str(similar_term), seedword)
                        if seq_score>levenshtein_threshold:
                            if not re.search(r'\_',similar_term):
                                vars[seedword].append(similar_term)
                                if not similar_term in all_expanded_terms and not similar_term in terms_to_expand:
                                    terms_to_expand.append(similar_term)
                except:
                        pass
                level+=1
        vars[seedword] = list(set(vars[seedword]))
    return vars

bias_stem_words_round_2 = pd.read_csv("word_list_round_2.csv")
bias_stem_words_round_2["similar_word"] = bias_stem_words_round_2["similar_word"].replace("_", " ", regex = True)

bias_expanded_word_list = bias_stem_words_round_2["similar_word"]


expanded = generate_spelling_variants(bias_expanded_word_list, model2, semantic_search_length=500, levenshtein_threshold = 0.85, setting = 1)

df = pd.DataFrame.from_dict(expanded, orient ='index')



df.to_csv("expanded_misspellings.csv")

