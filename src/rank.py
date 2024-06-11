from PyPDF2 import PdfReader
import streamlit as st
from embeddings import text_embedding
import scipy


def extract_and_rank(resumes, job_description):
    out_embed_dict = {}
    out_text_dict = {}
    for resume in resumes:
        reader = PdfReader(resume)
        raw_text = "".join(page.extract_text() for page in reader.pages)
        embedding = text_embedding(raw_text)
        d1 = {resume.name: (embedding)}
        d2 = {resume.name: raw_text}
        out_embed_dict.update(d1)
        out_text_dict.update(d2)
    ranked_output = rankings(out_dict=out_embed_dict, query=job_description)
    return ranked_output, out_embed_dict, out_text_dict


def get_sim(query_embedding, average_vec):
    try:
        sim = [(1 - scipy.spatial.distance.cosine(query_embedding, average_vec))]
        return sim
    except:
        return [0]


def rankings(out_dict, query):
    query_embedding = text_embedding(query)
    rank = []
    for k, v in out_dict.items():
        rank.append((k, get_sim(query_embedding, v)))
    rank = sorted(rank, key=lambda t: t[1], reverse=True)
    return rank


# def data_clean(text):
#     pattern = r'[^a-zA-Z0-9\s]'
#     text = re.sub(pattern,'',' '.join(text))
#     tokens = [token.strip() for token in text.split()]
#     filtered = [token for token in tokens if token.lower() not in stopword_list]
#     filtered = ' '.join(filtered)
#     return filtered


# def embeddings(word):
#     # print(word)
#     if word in wv.key_to_index:
#         return wv.get_vector(word)
#     else:
#         return np.zeros(300)