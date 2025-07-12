from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load Hugging Face grammar model
tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")

def correct_sentence(text):
    try:
        input_text = "gec: " + text
        input_ids = tokenizer.encode(input_text, return_tensors="pt", truncation=True)
        outputs = model.generate(input_ids, max_length=64, num_beams=5, early_stopping=True)
        corrected = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return corrected
    except Exception as e:
        print("⚠️ Grammar correction error:", e)
        return text
