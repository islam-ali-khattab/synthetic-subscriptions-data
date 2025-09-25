# Subscriptions Synthetic Data Generator  

A Python-based tool to generate **realistic subscription datasets** for analytics, dashboards, testing, and machine learning experiments.  

This generator simulates user subscriptions across multiple countries, plans, promotions, currencies, and payment methods. It produces a clean, ready-to-use dataset (`data.csv`).  

---

## 🚀 Features  

- **Synthetic Subscriptions** – Generates up to 50K subscriptions and 40K unique users.  
- **Global Coverage** – Supports multiple countries (Egypt, KSA, UAE, USA, UK, Spain, Germany, France).  
- **Flexible Plans** – Monthly, Quarterly, Biannual, and Annual plans with realistic prices.  
- **Currency Support** – Local currencies + optional conversion rates to USD.  
- **Discounts & Promotions** – Includes multiple promo codes with varying discount percentages.  
- **Payment Methods** – Online cards, bank transfers, digital wallets, and BNPL with country-specific providers.  
- **Living Standard Adjustments** – Subscription prices are adjusted based on cost of living multipliers.  
- **Complete Subscription Lifecycle** – Subscription, activation, expiration, and renewals simulated.  

---

## ⚙️ Configuration  

Modify constants in the script to customize:  

- `NUM_SUBS` → number of subscriptions to generate  
- `NUM_USERS` → number of unique users  
- `countries`, `plans`, `currency_map`, `promotions`, etc.  

---

## 📂 Output Schema  

- **user_id** → unique user identifier  
- **subscribtion_date** → date subscription was purchased  
- **activation_date** → when subscription became active  
- **expiration_date** → when subscription ends  
- **plan** → subscription plan (Monthly/Quarterly/Biannual/Annual)  
- **payment_method** → payment channel used  
- **payment_provider** → provider for that method in user’s country  
- **currency** → local currency of user  
- **base_price** → price before discount  
- **paid_amount** → final amount after discount  
- **promotion** → promo code applied (if any)  
- **discount_percentage** → discount %  
- **country** → user’s country  

---

## 🔮 Use Cases  

- Build & test dashboards (Streamlit, Power BI, Tableau).  
- Train machine learning models on customer behavior.  
- Stress-test ETL pipelines.  
- Run analytics experiments without sensitive data.  
