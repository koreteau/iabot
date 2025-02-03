from llama_cpp import Llama
import os
import re
import pandas as pd

llm = Llama(model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf", n_ctx=2048)
print("Modèle chargé avec succès !")

