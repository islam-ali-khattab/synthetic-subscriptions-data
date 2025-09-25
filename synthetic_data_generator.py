import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

random.seed(42)
np.random.seed(42)

NUM_SUBS = 50000
NUM_USERS = 40000  # number of unique users to create (will be reused to create renewals)

# 1) Helper data
countries = [
    "Egypt",  "Saudi Arabia", "United Arab Emirates", "United States",
    "United Kingdom", "Spain", "Germany", "France"
]

# Currency by country (simple mapping)
currency_map = {
    "Egypt": "EGP",
    "Saudi Arabia": "SAR",
    "United Arab Emirates": "AED",
    "United States": "USD",
    "United Kingdom": "GBP",
    "Spain": "EUR", 
    "Germany": "EUR",  
    "France": "EUR"   
}

# Plans and their durations (months)
plans = {
    "Monthly": 1,
    "Quarterly": 3,    
    "Biannual": 6,
    "Annual": 12
}

# Base prices for plans (in local currency)
plans_price = {
    "Monthly": 1200,
    "Quarterly": 3000,    
    "Biannual": 5400,
    "Annual": 10500
}

# Currency conversion to USD (للاستخدام فقط لو عايز تضيف عمود USD)
currency_conversion = {
    "EGP": 1,        
    "USD": 47.15,
    "SAR": 12.84,
    "AED": 13.10,
    "GBP": 65.57,
    "EUR": 56.58,
}

# Promotions with discount percentages
promotions = {
    "DISCOUNT5": 5.0,
    "DISCOUNT10": 10.0,
    "DISCOUNT15": 15.0,
    "DISCOUNT20": 20.0,
    "DISCOUNT25": 25.0,
    "DISCOUNT30": 30.0,
    "DISCOUNT40": 40.0,
    "DISCOUNT50": 50.0,   
}

# Payment methods
payment_methods = [
    "online_card",
    "bank_transfer",
    "digital_wallet",
    "buy_now_pay_later",
]

# Payment providers for each method by country
payment_providers_map = {
    "online_card": {
        "Egypt": ["paypal", "visa", "mastercard", "Meeza"],
        "Saudi Arabia": ["paypal", "visa", "mastercard", "stripe"],
        "United Arab Emirates": ["paypal", "visa", "mastercard"],
        "United States": ["paypal", "visa", "mastercard", "stripe"],
        "United Kingdom": ["paypal", "visa", "mastercard"],
        "Spain": ["paypal", "visa", "mastercard"],
        "Germany": ["paypal", "visa", "mastercard"],
        "France": ["paypal", "visa", "mastercard"]
    },
    "bank_transfer": {
        "Egypt": ["kashier", "local_gateway"],
        "Saudi Arabia": ["local_gateway", "SWIFT", "ACH"],
        "United Arab Emirates": ["local_gateway", "SWIFT"],
        "United States": ["ACH", "SWIFT", "local_gateway"],
        "United Kingdom": ["ACH", "local_gateway"],
        "Spain": ["SWIFT", "local_gateway"],
        "Germany": ["SWIFT", "local_gateway"],
        "France": ["SWIFT", "local_gateway"]
    },
    "digital_wallet": {
        "Egypt": ["vodafone_cash", "etisalat_cash", "paypal"],
        "Saudi Arabia": ["paypal", "apple_pay", "google_pay"],
        "United Arab Emirates": ["apple_pay", "google_pay", "paypal"],
        "United States": ["apple_pay", "google_pay", "paypal", "venmo"],
        "United Kingdom": ["apple_pay", "google_pay", "paypal"],
        "Spain": ["apple_pay", "google_pay", "paypal"],
        "Germany": ["apple_pay", "google_pay", "paypal"],
        "France": ["apple_pay", "google_pay", "paypal"]
    },
    "buy_now_pay_later": {
        "Egypt": ["Value", "souhoola"],
        "Saudi Arabia": ["Value", "Tamara", "Tabby"],
        "United Arab Emirates": ["Value", "Tamara", "Tabby"],
        "United States": ["Affirm", "Afterpay", "Klarna"],
        "United Kingdom": ["Klarna", "Clearpay"],
        "Spain": ["Klarna", "Afterpay"],
        "Germany": ["Klarna"],
        "France": ["Klarna", "Afterpay"]
    }
}

# Define living standard multipliers for price adjustment based on country
living_standard_multiplier = {
    "Egypt": 1.0,
    "Saudi Arabia": 2.2,        # افتراض تقريبي: السعودية أغلى من مصر لكن مش بقيمة الإمارات أو أمريكا
    "United Arab Emirates": 3.27,  # لأن 227٪ زيادة → يعني تقريبًا 3.27×
    "United States": 3.54,     # لأن 254٪ زيادة → يعني تقريبا 3.54×
    "United Kingdom": 2.8,     # تقدير بناءً على أن تكلفة المعيشة أعلى من معظم الدول العربية لكن أقل من أمريكا
    "Spain": 2.5,              # تقدير مشابه للمملكة المتحدة لكن شوية أقل
    "Germany": 3.0,            # مشابه لأمريكا لكن أقل شوية
    "France": 2.9              # قريب من ألمانيا/المملكة المتحدة
}


def generate_unique_user_ids(n):
    ids = set()
    while len(ids) < n:
        ids.add(f"U-{random.randint(100000, 999999)}")
    return list(ids)

user_ids = generate_unique_user_ids(NUM_USERS)

def random_date(start, end):
    """Return random datetime between start and end (inclusive)."""
    delta = end - start
    rand_days = random.randint(0, delta.days)
    rand_seconds = random.randint(0, 86400 - 1)
    return start + timedelta(days=rand_days, seconds=rand_seconds)

start_date = datetime(2021, 1, 1)
end_date = datetime(2025, 8, 31, 23, 59, 59)

# Track countries assigned to users to ensure they stay within the same country
user_country_map = {}

rows = []
for i in range(NUM_SUBS):
    # Pick or create a student (re-using to simulate renewals)
    user_id = random.choice(user_ids)

    # Ensure the user subscribes in the same country
    if user_id not in user_country_map:
        country = random.choices(countries, weights = [0.25, 0.20, 0.15, 0.10, 0.10, 0.08, 0.07, 0.05], k=1)[0]
        user_country_map[user_id] = country
    else:
        country = user_country_map[user_id]
    
    currency = currency_map[country]

    # Subscription date
    subscribtion_date = random_date(start_date, end_date)

    # Activation date
    activation_delay_days = random.choices([0,1,2,3,4,5,7,10,14], weights=[30,20,15,10,8,5,4,4,4], k=1)[0]
    activation_date = subscribtion_date + timedelta(days=activation_delay_days)

    # Plan selection
    plan = random.choices(list(plans.keys()), weights=[0.5, 0.25, 0.15, 0.1] , k=1)[0]
    duration_months = plans[plan]

    # Expiration date
    expiration_date = (activation_date + relativedelta(months=duration_months)) - timedelta(days=1)

    # Promotion
    promo = random.choices(list(promotions.keys()) + ["NONE"], 
                            weights=[0.2, 0.2, 0.15, 0.05, 0.05, 0.03, 0.04, 0.03, 0.25], k=1)[0]
    discount_pct = promotions.get(promo, 0)

    # Base price in local currency
    Plan_price = plans_price[plan] / currency_conversion[currency_map[country]]

    # Adjust price for living standards
    multiplier = living_standard_multiplier.get(country, 1.0)
    base_price = round(Plan_price * multiplier, 0)

    # Apply discount
    discounted_amount = round(base_price - (base_price * (1 - discount_pct/100.0)), 2)

    # Payment method & provider
    payment_method = random.choices(payment_methods, weights=[0.25,0.25,0.25,0.25], k=1)[0]
    payment_provider = random.choice(payment_providers_map[payment_method][country])

    # كل المستخدمين بيدفعوا المبلغ كامل بعد الخصم
    paid_amount = round(base_price * (1 - discount_pct/100.0), 2)

    # No refunds
    refund_date = pd.NaT

    rows.append({
        "user_id": user_id,
        "subscribtion_date": subscribtion_date,
        "activation_date": activation_date,
        "expiration_date": expiration_date,
        "plan": plan,
        "refund_date": refund_date,
        "payment_method": payment_method,
        "payment_provider": payment_provider,
        "currency": currency,
        "paid_amount": paid_amount,
        "base_price": base_price,
        "discounted_amount": discounted_amount,
        "promotion": promo if promo != "NONE" else "",
        "discount_percentage": discount_pct,
        "country": country
    })

df = pd.DataFrame(rows)

df.to_csv("data.csv", index=False)
print("Data generated and saved to data.csv")
