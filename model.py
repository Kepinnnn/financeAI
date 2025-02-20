from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_expense(description):
    labels = ["Makanan", "Transportasi", "Belanja", "Tagihan", "Hiburan"]
    result = classifier(description, labels)
    return result['labels'][0]  # Mengambil label dengan skor tertinggi
