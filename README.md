# Mastercard Career Chatbot: NLP Optimization & Fixes

An advanced NLP pipeline designed to solve 9 critical edge-case failures identified during black-box testing of Mastercard's live career chatbot. This repository features an optimized intent classifier supporting Hinglish, automated spell correction, and fallback thresholding, deployed as an interactive Streamlit application.

---

## 🚀 The Story (Recruiter Breakdown)

### 1. The Problem
While exploring Mastercard's live career chatbot, I noticed it failed on basic operational inputs. Queries like *"Hi"*, *"help me"*, and *"what can you do"* consistently returned error messages instead of routing users correctly. I decided to formally audit and test it.

### 2. What I Did
I conducted rigorous black-box testing using 30+ varied inputs across multiple risk categories: typos, Hinglish syntax, out-of-scope queries, and basic conversational greetings. I documented every breakdown to identify the exact root causes in intent recognition, multilingual workflows, and fallback handling.

### 3. What I Built
I built a completely redesigned NLP pipeline using Python. The architecture implements TF-IDF vectorization, token lemmatization, and customized stopword elimination feeding into an optimized Logistic Regression and SVM classifier. To protect user experience, I integrated:
* **Hinglish Code-Switching Support**: Built specifically for the large percentage of Indian users typing in mixed languages.
* **Custom Hinglish-Safe Spell Correction**: A filter preventing standard English engines from damaging code-switched phrases.
* **Confidence Thresholding**: Prevents wild misclassifications by routing ambiguous text to a clean fallback loop.

### 4. The Results
The upgraded pipeline achieved an **85% test accuracy** and an **83% cross-validation score** across 9 distinct career intents using 785 high-density training samples. Every single test case where the original production bot broke is now handled seamlessly.

---

## 🛠️ Technical Architecture

### Tech Stack
* **Language**: Python 3.10+
* **NLP & ML Engine**: Scikit-learn, NLTK, TextBlob
* **Frontend Demo**: Streamlit

### Pipeline Evaluation Metrics
* **Dataset Size**: 785 curated training tokens
* **Validation Strategy**: Stratified K-Fold Cross-Validation
* **Target Metric**: 85% Accuracy across 9 intents

---

## 📊 Live Failure Case Auditing

This project completely eliminates the 9 critical structural gaps uncovered in the production system:


| Identified Failure Category | Original Live Bot Response | Optimized Pipeline Performance |
| :--- | :--- | :--- |
| **Basic Greetings** (*"Hi"*) | Fallback Error | Mapped to `Greeting` Intent |
| **Help Requests** (*"Help me"*) | Fallback Error | Mapped to `Help` Intent |
| **Capabilities Discovery** (*"What can you do?"*) | Fallback Error | Mapped to `Capabilities` Intent |
| **Typographical Variations** (*"Appli for job"*) | Misclassification | Corrected via custom text filter |
| **Hinglish Code-Switching** (*"Job kaise apply kare"*) | Fallback Error | Classified under `Application_Process` |
| **Out-of-Scope Queries** (*"Weather today"*) | Erroneous Output | Gracefully rejected via confidence threshold |

---

## 💻 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com
   cd mastercard-career-chatbot
   ```

2. **Install core dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download required NLTK corpuses**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
   ```

4. **Launch the application UI**
   ```bash
   streamlit run app.py
   ```

---

Author
**Devansh**
