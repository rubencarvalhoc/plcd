import spacy

nlp = spacy.load("pt_core_news_sm")

text = ("O Gustavo comeu uma sopa e uma sandes.")
doc = nlp(text)


print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])


for entity in doc.ents:
    print(entity.text, entity.label_)
