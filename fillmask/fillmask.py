from transformers  import AutoModelForMaskedLM,AutoTokenizer,pipeline
modelmask = AutoModelForMaskedLM.from_pretrained('neuralmind/bert-large-portuguese-cased')
tokenizermask = AutoTokenizer.from_pretrained('neuralmind/bert-large-portuguese-cased', do_lower_case=False)

pipe = pipeline('fill-mask', model=modelmask, tokenizer=tokenizermask)
print()
print()
print(pipe('[MASK] era Jesus?'))
#nlpner = pipeline('ner', model=modelner, tokenizer=tokenizerner, grouped_entities=True)


input_txt = "[MASK] [MASK] era Jesus?"
inputs = tokenizermask(input_txt, return_tensors='pt')
outputs = modelmask(**inputs)
predictions = outputs[0]
sorted_preds, sorted_idx = predictions[0].sort(dim=-1, descending=True)
print(input_txt)
for k in range(10):

    sortedsidx=[]
    for i in range(0,len(sorted_idx)):

        sortedsidx.append(sorted_idx[i, k].item())
    predicted_index=sortedsidx
    #predicted_index = [sorted_idx[i, k].item() for i in range(0,24)]
    predicted_token = [tokenizermask.convert_ids_to_tokens([predicted_index[x]])[0] for x in range(1,len(sorted_idx))]
    print(predicted_token)