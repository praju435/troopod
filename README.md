# 🚀 Troopod – AI-Powered Landing Page Personalization

A system that enhances existing landing pages based on ad intent using CRO (Conversion Rate Optimization) principles.

---

## 🔗 Live Demo
👉 https://your-app.netlify.app  

## 📄 Explanation Doc
👉 https://your-google-doc-link  

---

## 🧠 Overview

Troopod bridges the gap between **ad creatives and landing page experience**.

Instead of generating new pages, it **enhances existing landing pages** by aligning them with the intent of the ad — improving conversions without redesign.

---

## ⚙️ How It Works

### 🔄 Flow

1. User inputs:
   - Ad (URL / text / image)
   - Landing page URL  

2. Backend:
   - Fetches landing page HTML  
   - Extracts base structure  

3. AI Processing:
   - Understands ad intent  
   - Optimizes:
     - Headlines  
     - CTA  
     - Messaging  

4. Output:
   - Returns improved HTML  
   - Frontend renders updated page  

---

## 🧩 Architecture

### 🔹 Fetch Layer
- Uses `httpx` to retrieve HTML  
- Handles redirects and base URLs  

### 🔹 Context Builder
- Converts ad input into structured intent  

### 🔹 CRO Optimization Engine
- AI-driven (Gemini/OpenAI)
- Focuses on:
  - Clarity  
  - Urgency  
  - Value proposition  

### 🔹 Output Processor
- Cleans AI response  
- Ensures valid HTML  

### 🔹 Frontend
- Displays personalized page  
- Shows user-friendly status updates  

---

## 🛠️ Tech Stack

- **Backend:** FastAPI  
- **Frontend:** HTML, JavaScript  
- **AI:** Gemini / OpenAI  
- **Deployment:** Render + Netlify  

---

## 🚧 Challenges & Solutions

### 🔄 Random Changes
- Controlled via strict prompt constraints  
- Focus only on messaging  

### 🧱 Broken UI
- Preserve original HTML structure  
- Inject `<base>` tag for assets  

### 🤖 Hallucinations
- Avoid unrealistic claims via prompt design  
- Keep outputs grounded  

### ⚖️ Inconsistent Outputs
- Standardized prompts  
- Defined CRO role  

---

## ⚡ Features

- Ad-to-page personalization  
- CRO-based optimization  
- Works on existing pages  
- Lightweight and fast  

---

## 🚀 Getting Started (Local)

### 1. Clone repo
```bash
git clone https://github.com/praju435/troopod.git
cd troopod
