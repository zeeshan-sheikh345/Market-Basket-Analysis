## 1. What is Market Basket Analysis?

**Market Basket Analysis** is a **data mining technique** used to discover **patterns of items that are frequently bought together** by customers.

> In simple words:
“If a customer buys X, what else are they likely to buy?”
> 

It is based on **association rule learning**.

---

## 2. Why is Market Basket Analysis Important in Marketing?

MBA helps marketers in:

### 🎯 Key Business Applications

- **Cross-selling & up-selling**
- **Product bundling**
- **Recommendation systems** (Amazon-style “Frequently Bought Together”)
- **Store layout optimization**
- **Promotion planning**
- **Email & push personalization**

### 📌 Example

If customers often buy:

- **Bread + Butter**
→ Offer a **combo discount** or place them nearby in store.

---

## 3. Real-World Examples

| Industry | Example |
| --- | --- |
| Retail | Bread → Butter |
| E-commerce | Phone → Phone Case |
| Banking | Savings Account → Credit Card |
| OTT | Series A → Series B |
| EdTech | Python Course → SQL Course |

---

## 4. Key Concepts & Terminology

### 4.1 Transaction

A **single purchase event** by a customer.

```
Transaction 1: Milk, Bread, Butter
Transaction 2: Bread, Eggs
```

---

### 4.2 Itemset

A **group of items**.

- {Bread}
- {Bread, Butter}
- {Milk, Bread, Butter}

---

## 5. Core concepts in Market Basket Analysis

### 1️⃣ What is Association Rule Mining?

**Association Rule Mining** is a data mining technique used to discover **relationships between items** in transactional data.

It answers questions like:

> “If a customer buys A, what is the likelihood they will also buy B?”
> 

An association rule is written as:

```
A → B

```

Meaning:

> Customers who buy A tend to also buy B
> 

---

### 2️⃣ Why Association Rules Are Used in MBA

In **Marketing Analytics**, association rules help in:

- Cross-selling
- Product bundling
- Recommendation systems
- Store layout optimization
- Personalized offers

### 3️⃣ Core Metrics in Association Rules

### 1. Support

**Support** = How frequently an itemset appears in the dataset.

!image.png

📌 Example:

```
Bread appears in 3 out of 5 transactions
Support(Bread) = 3/5 = 0.6

```

---

### 2. Confidence

**Confidence** = Probability of buying B **given** that A was bought.

!image.png

📌 Example:

```
Out of customers who bought Bread,
80% also bought Butter

```

---

### 3. Lift (Most Important)

**Lift** measures **how much more likely** B is bought when A is bought **compared to random chance**.

!image.png

| Lift Value | Interpretation |
| --- | --- |
| > 1 | Positive association (good rule) |
| = 1 | No association |
| < 1 | Negative association |

📌 Marketers mostly care about **Lift > 1**

---

## 6. Sample Dataset (Transactions)

Assume we have **5 customers’ purchase data**:

| Transaction ID | Items Purchased |
| --- | --- |
| T1 | Milk, Bread, Butter |
| T2 | Bread, Eggs |
| T3 | Milk, Bread, Butter |
| T4 | Milk, Eggs |
| T5 | Bread, Butter |

Total transactions = **5**

---

## 7. Step-by-Step Market Basket Analysis

### Step 1: Calculate Support

### Individual Items

| Item | Transactions | Support |
| --- | --- | --- |
| Milk | T1, T3, T4 | 3/5 = 0.6 |
| Bread | T1, T2, T3, T5 | 4/5 = 0.8 |
| Butter | T1, T3, T5 | 3/5 = 0.6 |
| Eggs | T2, T4 | 2/5 = 0.4 |

---

### Item Pairs

| Itemset | Transactions | Support |
| --- | --- | --- |
| Bread + Butter | T1, T3, T5 | 3/5 = 0.6 |
| Milk + Bread | T1, T3 | 2/5 = 0.4 |
| Milk + Butter | T1, T3 | 2/5 = 0.4 |
| Bread + Eggs | T2 | 1/5 = 0.2 |

---

### Step 2: Create Association Rules

### Rule 1: Bread → Butter

- Support(Bread, Butter) = 0.6
- Support(Bread) = 0.8
`Confidence = 0.6 / 0.8 = 0.75`
- Support(Butter) = 0.6 
`Lift = 0.75 / 0.6 = 1.25`

✅ **Strong & useful rule**

### Rule 2: Milk → Bread

- Support(Milk, Bread) = 0.4
- Support(Milk) = 0.6
`Confidence = 0.4 / 0.6 = 0.67
Lift = 0.67 / 0.8 = 0.84`

❌ Weak rule (Lift < 1)

---

## 8. Interpretation for Marketers

### 📈 Best Rule Found

```
Bread → Butter
Support: 60%
Confidence: 75%
Lift: 1.25
```

### 🧠 Marketing Insights

- Customers buying **Bread** are **25% more likely** to buy Butter than average.
- Place Butter near Bread.
- Create Bread-Butter combo.
- Recommend Butter when Bread is added to cart.

---

## 9. Algorithms Used in Market Basket Analysis

### 9.1 Apriori Algorithm (Most Common)

- Generates frequent itemsets.
- Uses **minimum support threshold.**
- Computationally expensive for large data.

### 9.2 FP-Growth Algorithm

- Faster than Apriori
- Used in large-scale systems (Amazon, Flipkart)

---

## 10. MBA in Digital Marketing Context

| Channel | Usage |
| --- | --- |
| Website | Product recommendations |
| Email | Cross-sell campaigns |
| Ads | Bundle-based targeting |
| CRM | Personalized offers |
| Mobile Apps | In-app suggestions |

---

## 11. Common Mistakes to Avoid

❌ Using only **confidence**
❌ Ignoring **lift**
❌ Very low support (noise)
❌ Treating correlation as causation

---

## 12. When NOT to Use Market Basket Analysis

- Very **small datasets**
- One-time purchases
- Highly seasonal products without segmentation

---

## 13. Summary

> Market Basket Analysis is an association rule mining technique used to identify relationships between products purchased together. It uses support, confidence, and lift to evaluate the strength of rules and is widely used in marketing for cross-selling, bundling, and recommendations.

> ---
