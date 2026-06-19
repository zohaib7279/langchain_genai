from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline

pipe = pipeline(
    "text-generation",
    model="gpt2",
    max_new_tokens=50,
    temperature=0.1, 
    num_return_sequences=1
)

llm = HuggingFacePipeline(pipeline=pipe)

# Specific prompt
response = llm.invoke("What is the capital of France?")
print(response)