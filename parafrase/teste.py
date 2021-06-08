from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('D:\\0000python\\squadbert\\distiluse-base-multilingual-cased-v1')
#kiri-ai/distiluse-base-multilingual-cased-et
sentences=['Deus te ama',
             'Deus é amor']
query_embedding = model.encode('Deus te ama.')
passage_embedding = model.encode('Você é amado por Deus.')
paraphrases = util.paraphrase_mining(model, sentences)

for paraphrase in paraphrases[0:10]:
    score, i, j = paraphrase
    print("{} \t\t {} \t\t Score: {:.4f}".format(sentences[i], sentences[j], score))


print("Similarity:", util.pytorch_cos_sim(query_embedding, passage_embedding))
