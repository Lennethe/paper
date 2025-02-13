import torch
from pytorch_transformers import BertTokenizer, BertModel, BertForNextSentencePrediction

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


def predictor(sentence1, sentence2):
    text = "[CLS] " + sentence1 + " [SEP] a" + sentence2 + " [SEP]"

    ids1 = [0] *(len(tokenizer.tokenize(sentence1)) + 2)
    ids2 = [1] *(len(tokenizer.tokenize(sentence2)) + 1)
    ids1.extend(ids2)
    
    tokenized_text = tokenizer.tokenize(text)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    segments_ids = ids1
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])
    
    model = BertForNextSentencePrediction.from_pretrained('bert-base-uncased')
    model.eval()

    tokens_tensor = tokens_tensor.to('cuda')
    segments_tensors = segments_tensors.to('cuda')
    model.to('cuda')

    # Predict the next sentence classification logits
    with torch.no_grad():
        next_sent_classif_logits = model(tokens_tensor, segments_tensors)

    ret = torch.softmax(next_sent_classif_logits[0], dim=1)
    a.cpu()
    return a[0][0].item()
