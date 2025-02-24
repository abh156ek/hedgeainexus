import requests

ALPACA_API_KEY = ""
ALPACA_SECRET_KEY = ""

HUGGINGFACE_API_KEY = ""

FINBERT_API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"

def get_news(ticker):
    url = f"https://data.alpaca.markets/v1beta1/news?symbols={ticker}&limit=5"
    headers = {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        news_data = response.json()
        if "news" in news_data:
            headlines = [article["headline"] for article in news_data["news"]]
            return headlines
        else:
            print("No 'news' key found in API response:", news_data)
            return []
    else:
        print(f"Error fetching news: {response.status_code}, {response.text}")
        return []

def analyze_sentiment_api(headlines):
    if not headlines:
        return 0.5  
    
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    sentiment_scores = []
    
    for headline in headlines:
        response = requests.post(FINBERT_API_URL, headers=headers, json={"inputs": headline})
        
        if response.status_code == 200:
            predictions = response.json()
            label = predictions[0][0]["label"]
            score = predictions[0][0]["score"]
            
            if label == "positive":
                sentiment_scores.append(score) 
            elif label == "negative":
                sentiment_scores.append(-score) 
            else:
                sentiment_scores.append(0)  
        else:
            print(f"Error analyzing sentiment: {response.status_code}, {response.text}")
            sentiment_scores.append(0)  
    
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    return round(avg_sentiment, 3)


ticker = "NVDA"
headlines = get_news(ticker)
print(f"Headlines for {ticker}:")
print(headlines)

sentiment_score = analyze_sentiment_api(headlines)
print(f"Sentiment Score for {ticker}: {sentiment_score}")
