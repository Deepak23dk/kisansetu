# KisanSetu - Mandi Market Prices Dataset
# Covers all 28 Indian States and key crops: rice, wheat, tomato, onion, cotton, sugarcane

MARKET_PRICES = {
    "andhra pradesh": {
        "rice": {"price_range": "₹3,200 - ₹3,900 per quintal", "mandi": "Nellore Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹15 - ₹22 per kg", "mandi": "Madanapalle Mandi", "trend": "Rising"},
        "cotton": {"price_range": "₹6,800 - ₹7,500 per quintal", "mandi": "Adoni Mandi", "trend": "Stable"},
        "sugarcane": {"price_range": "₹3,150 - ₹3,400 per ton", "mandi": "Chittoor Mandi", "trend": "Stable"},
        "onion": {"price_range": "₹14 - ₹20 per kg", "mandi": "Kurnool Mandi", "trend": "Falling"}
    },
    "arunachal pradesh": {
        "rice": {"price_range": "₹3,500 - ₹4,200 per quintal", "mandi": "Naharlagun Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹30 - ₹45 per kg", "mandi": "Pasighat Mandi", "trend": "Rising"},
        "wheat": {"price_range": "₹2,400 - ₹2,800 per quintal", "mandi": "Along Mandi", "trend": "Stable"}
    },
    "assam": {
        "rice": {"price_range": "₹2,800 - ₹3,400 per quintal", "mandi": "Guwahati Mandi", "trend": "Rising"},
        "sugarcane": {"price_range": "₹3,000 - ₹3,300 per ton", "mandi": "Jorhat Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹25 - ₹35 per kg", "mandi": "Silchar Mandi", "trend": "Stable"}
    },
    "bihar": {
        "rice": {"price_range": "₹2,400 - ₹3,100 per quintal", "mandi": "Gulabbagh Mandi", "trend": "Rising"},
        "wheat": {"price_range": "₹2,100 - ₹2,400 per quintal", "mandi": "Patna Mandi", "trend": "Stable"},
        "sugarcane": {"price_range": "₹3,100 - ₹3,350 per ton", "mandi": "Motihari Mandi", "trend": "Stable"},
        "onion": {"price_range": "₹12 - ₹18 per kg", "mandi": "Bihar Sharif Mandi", "trend": "Falling"}
    },
    "chhattisgarh": {
        "rice": {"price_range": "₹2,200 - ₹2,800 per quintal", "mandi": "Raipur Mandi", "trend": "Stable"},
        "sugarcane": {"price_range": "₹3,050 - ₹3,300 per ton", "mandi": "Kabirdham Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹14 - ₹20 per kg", "mandi": "Durg Mandi", "trend": "Falling"}
    },
    "goa": {
        "rice": {"price_range": "₹3,000 - ₹3,800 per quintal", "mandi": "Margao Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹30 - ₹45 per kg", "mandi": "Mapusa Mandi", "trend": "Rising"},
        "onion": {"price_range": "₹25 - ₹35 per kg", "mandi": "Panaji Mandi", "trend": "Stable"}
    },
    "gujarat": {
        "cotton": {"price_range": "₹7,000 - ₹7,900 per quintal", "mandi": "Rajkot Mandi", "trend": "Rising"},
        "onion": {"price_range": "₹10 - ₹16 per kg", "mandi": "Mahuva Mandi", "trend": "Falling"},
        "wheat": {"price_range": "₹2,400 - ₹2,900 per quintal", "mandi": "Gondal Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹15 - ₹22 per kg", "mandi": "Ahmedabad Mandi", "trend": "Stable"}
    },
    "haryana": {
        "wheat": {"price_range": "₹2,275 - ₹2,450 per quintal", "mandi": "Karnal Mandi", "trend": "Rising"},
        "rice": {"price_range": "₹3,800 - ₹4,800 per quintal", "mandi": "Kurukshetra Mandi", "trend": "Stable"},
        "cotton": {"price_range": "₹6,700 - ₹7,400 per quintal", "mandi": "Sirsa Mandi", "trend": "Stable"},
        "sugarcane": {"price_range": "₹3,400 - ₹3,620 per ton", "mandi": "Rohtak Mandi", "trend": "Stable"}
    },
    "himachal pradesh": {
        "tomato": {"price_range": "₹25 - ₹40 per kg", "mandi": "Solan Mandi", "trend": "Rising"},
        "wheat": {"price_range": "₹2,300 - ₹2,600 per quintal", "mandi": "Kangra Mandi", "trend": "Stable"},
        "onion": {"price_range": "₹20 - ₹28 per kg", "mandi": "Shimla Mandi", "trend": "Stable"}
    },
    "jharkhand": {
        "rice": {"price_range": "₹2,500 - ₹3,200 per quintal", "mandi": "Ranchi Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹18 - ₹26 per kg", "mandi": "Hazaribagh Mandi", "trend": "Stable"},
        "onion": {"price_range": "₹15 - ₹22 per kg", "mandi": "Jamshedpur Mandi", "trend": "Falling"}
    },
    "karnataka": {
        "rice": {"price_range": "₹3,600 - ₹4,500 per quintal", "mandi": "Shimoga Mandi", "trend": "Rising"},
        "tomato": {"price_range": "₹22 - ₹30 per kg", "mandi": "Kolar Mandi", "trend": "Rising"},
        "onion": {"price_range": "₹15 - ₹22 per kg", "mandi": "Yeshwanthpur Mandi", "trend": "Stable"},
        "cotton": {"price_range": "₹6,800 - ₹7,600 per quintal", "mandi": "Raichur Mandi", "trend": "Stable"},
        "sugarcane": {"price_range": "₹3,150 - ₹3,350 per ton", "mandi": "Belgaum Mandi", "trend": "Stable"}
    },
    "kerala": {
        "rice": {"price_range": "₹3,000 - ₹3,700 per quintal", "mandi": "Palakkad Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹35 - ₹50 per kg", "mandi": "Ernakulam Mandi", "trend": "Rising"},
        "sugarcane": {"price_range": "₹3,200 - ₹3,500 per ton", "mandi": "Marayoor Mandi", "trend": "Stable"}
    },
    "madhya pradesh": {
        "wheat": {"price_range": "₹2,300 - ₹2,700 per quintal", "mandi": "Indore Mandi", "trend": "Rising"},
        "onion": {"price_range": "₹8 - ₹14 per kg", "mandi": "Indore Mandi", "trend": "Falling"},
        "cotton": {"price_range": "₹6,500 - ₹7,200 per quintal", "mandi": "Khargone Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹12 - ₹18 per kg", "mandi": "Jabalpur Mandi", "trend": "Stable"}
    },
    "maharashtra": {
        "onion": {"price_range": "₹15 - ₹22 per kg", "mandi": "Lasalgaon Mandi", "trend": "Rising"},
        "tomato": {"price_range": "₹20 - ₹28 per kg", "mandi": "Nashik Mandi", "trend": "Stable"},
        "cotton": {"price_range": "₹7,000 - ₹7,750 per quintal", "mandi": "Yavatmal Mandi", "trend": "Rising"},
        "sugarcane": {"price_range": "₹3,200 - ₹3,450 per ton", "mandi": "Kolhapur Mandi", "trend": "Stable"},
        "rice": {"price_range": "₹3,500 - ₹4,200 per quintal", "mandi": "Nagpur Mandi", "trend": "Stable"}
    },
    "manipur": {
        "rice": {"price_range": "₹3,200 - ₹3,800 per quintal", "mandi": "Imphal Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹30 - ₹42 per kg", "mandi": "Thoubal Mandi", "trend": "Rising"}
    },
    "meghalaya": {
        "rice": {"price_range": "₹3,400 - ₹4,000 per quintal", "mandi": "Shillong Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹28 - ₹38 per kg", "mandi": "Tura Mandi", "trend": "Stable"}
    },
    "mizoram": {
        "rice": {"price_range": "₹3,600 - ₹4,300 per quintal", "mandi": "Aizawl Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹35 - ₹48 per kg", "mandi": "Lunglei Mandi", "trend": "Stable"}
    },
    "nagaland": {
        "rice": {"price_range": "₹3,500 - ₹4,100 per quintal", "mandi": "Dimapur Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹32 - ₹45 per kg", "mandi": "Kohima Mandi", "trend": "Rising"}
    },
    "odisha": {
        "rice": {"price_range": "₹2,183 - ₹2,500 per quintal", "mandi": "Bargarh Mandi", "trend": "Stable"},
        "sugarcane": {"price_range": "₹3,000 - ₹3,200 per ton", "mandi": "Nayagarh Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹16 - ₹24 per kg", "mandi": "Cuttack Mandi", "trend": "Stable"}
    },
    "punjab": {
        "wheat": {"price_range": "₹2,275 - ₹2,400 per quintal", "mandi": "Khanna Mandi", "trend": "Rising"},
        "rice": {"price_range": "₹3,800 - ₹4,500 per quintal", "mandi": "Amritsar Mandi", "trend": "Stable"},
        "cotton": {"price_range": "₹6,900 - ₹7,600 per quintal", "mandi": "Bathinda Mandi", "trend": "Stable"},
        "sugarcane": {"price_range": "₹3,400 - ₹3,600 per ton", "mandi": "Jalandhar Mandi", "trend": "Stable"}
    },
    "rajasthan": {
        "wheat": {"price_range": "₹2,275 - ₹2,500 per quintal", "mandi": "Kota Mandi", "trend": "Rising"},
        "onion": {"price_range": "₹10 - ₹16 per kg", "mandi": "Alwar Mandi", "trend": "Falling"},
        "cotton": {"price_range": "₹6,700 - ₹7,400 per quintal", "mandi": "Sri Ganganagar Mandi", "trend": "Stable"}
    },
    "sikkim": {
        "rice": {"price_range": "₹3,400 - ₹4,100 per quintal", "mandi": "Gangtok Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹30 - ₹45 per kg", "mandi": "Namchi Mandi", "trend": "Stable"}
    },
    "tamil nadu": {
        "rice": {"price_range": "₹3,400 - ₹4,200 per quintal", "mandi": "Trichy Mandi", "trend": "Rising"},
        "tomato": {"price_range": "₹18 - ₹26 per kg", "mandi": "Ottanchatram Mandi", "trend": "Stable"},
        "cotton": {"price_range": "₹7,000 - ₹7,800 per quintal", "mandi": "Konganapuram Mandi", "trend": "Stable"},
        "sugarcane": {"price_range": "₹3,150 - ₹3,400 per ton", "mandi": "Erode Mandi", "trend": "Stable"},
        "onion": {"price_range": "₹20 - ₹28 per kg", "mandi": "Coimbatore Mandi", "trend": "Rising"}
    },
    "telangana": {
        "rice": {"price_range": "₹2,800 - ₹3,500 per quintal", "mandi": "Suryapet Mandi", "trend": "Stable"},
        "cotton": {"price_range": "₹6,900 - ₹7,650 per quintal", "mandi": "Warangal Mandi", "trend": "Rising"},
        "tomato": {"price_range": "₹16 - ₹24 per kg", "mandi": "Bowenpally Mandi", "trend": "Stable"}
    },
    "tripura": {
        "rice": {"price_range": "₹3,000 - ₹3,600 per quintal", "mandi": "Agartala Mandi", "trend": "Stable"},
        "tomato": {"price_range": "₹26 - ₹36 per kg", "mandi": "Udaipur Mandi", "trend": "Stable"}
    },
    "uttar pradesh": {
        "wheat": {"price_range": "₹2,275 - ₹2,450 per quintal", "mandi": "Hapur Mandi", "trend": "Stable"},
        "potato": {"price_range": "₹12 - ₹18 per kg", "mandi": "Agra Mandi", "trend": "Rising"},
        "sugarcane": {"price_range": "₹3,400 - ₹3,550 per ton", "mandi": "Meerut Mandi", "trend": "Stable"},
        "rice": {"price_range": "₹2,600 - ₹3,300 per quintal", "mandi": "Gorakhpur Mandi", "trend": "Stable"},
        "onion": {"price_range": "₹14 - ₹20 per kg", "mandi": "Kanpur Mandi", "trend": "Falling"}
    },
    "uttarakhand": {
        "wheat": {"price_range": "₹2,275 - ₹2,480 per quintal", "mandi": "Kashipur Mandi", "trend": "Stable"},
        "rice": {"price_range": "₹2,800 - ₹3,600 per quintal", "mandi": "Haldwani Mandi", "trend": "Stable"},
        "sugarcane": {"price_range": "₹3,350 - ₹3,500 per ton", "mandi": "Kichha Mandi", "trend": "Stable"}
    },
    "west bengal": {
        "rice": {"price_range": "₹2,600 - ₹3,400 per quintal", "mandi": "Burdwan Mandi", "trend": "Rising"},
        "tomato": {"price_range": "₹20 - ₹28 per kg", "mandi": "Sheoraphuly Mandi", "trend": "Stable"},
        "sugarcane": {"price_range": "₹3,100 - ₹3,300 per ton", "mandi": "Nadia Mandi", "trend": "Stable"}
    }
}
