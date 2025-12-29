import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey everyone! My name is Arpit Yadav"

tokens = enc.encode(text)

print("tokens : ",tokens)

detokenize = enc.decode([25216, 6524, 0, 3673, 1308, 382, 1754, 31300, 865, 110810, 76865])

print("detokenize : ",detokenize)