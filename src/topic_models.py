# src/topic_models.py
from typing import List, Tuple, Dict
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel

def build_bow(texts: List[str], max_features=5000, min_df=5):
    cv = CountVectorizer(max_features=max_features, min_df=min_df)
    X = cv.fit_transform(texts); return X, cv

def build_tfidf(texts: List[str], max_features=5000, min_df=5):
    tv = TfidfVectorizer(max_features=max_features, min_df=min_df)
    X = tv.fit_transform(texts); return X, tv

def train_lda_bow(X, n_topics: int, random_state=42):
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=random_state, learning_method="batch")
    return lda.fit(X)

def train_nmf_tfidf(X, n_topics: int, random_state=42):
    nmf = NMF(n_components=n_topics, random_state=random_state, init="nndsvda", max_iter=400)
    return nmf.fit(X)

def top_words_per_topic(model, feature_names: List[str], topn=10):
    topics = []
    for comp in model.components_:
        idx = np.argsort(comp)[::-1][:topn]
        topics.append([feature_names[i] for i in idx])
    return topics

def coherence_cv(tokenized_texts: List[List[str]], topics_words: List[List[str]]) -> float:
    dictionary = Dictionary(tokenized_texts)
    cm = CoherenceModel(topics=topics_words, texts=tokenized_texts, dictionary=dictionary, coherence='c_v')
    return float(cm.get_coherence())

def grid_coherence_lda(texts: List[str], tokenized: List[List[str]], k_list: List[int]) -> Dict[int, float]:
    X_bow, cv = build_bow(texts)
    feats = cv.get_feature_names_out().tolist()
    res = {}
    for k in k_list:
        model = train_lda_bow(X_bow, k)
        res[k] = coherence_cv(tokenized, top_words_per_topic(model, feats, 10))
    return res

def grid_coherence_nmf(texts: List[str], tokenized: List[List[str]], k_list: List[int]) -> Dict[int, float]:
    X_tfidf, tv = build_tfidf(texts)
    feats = tv.get_feature_names_out().tolist()
    res = {}
    for k in k_list:
        model = train_nmf_tfidf(X_tfidf, k)
        res[k] = coherence_cv(tokenized, top_words_per_topic(model, feats, 10))
    return res
