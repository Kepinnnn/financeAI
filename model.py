from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# Use a pipeline as a high-level helper
sentiment_pipeline = pipeline("text-classification", model="ProsusAI/finbert")


def classify_expense(description):
    labels = ["Makanan", "Transportasi", "Belanja", "Tagihan", "Hiburan"]
    result = classifier(description, labels)
    return result['labels'][0]  # Mengambil label dengan skor tertinggi

def analyze_spending_trend(descriptions):

    # Menganalisis sentimen dari daftar deskripsi pengeluaran

    results = sentiment_pipeline(descriptions)
    
    # Hitung jumlah kategori sentimen (positif, netral, negatif)
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}

    for result in results:
        sentiment = result["label"].lower()
        sentiment_counts[sentiment] += 1

    return sentiment_counts
