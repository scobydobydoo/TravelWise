<h1 align="center">TravelWise </h1>

<p align="center">
  <img src="assets/eeea21c2-8a22-40e2-a222-e33285d345dd.png" width="400" alt="ProjectWise Logo"/>
</p>

<p align="center">
Intelligent Tourist Assistance and Decision Support Platform
</p>

<p align="center">
  <img src="https://img.shields.io/badge/cpp-3.10-blue" />
  <img src="https://img.shields.io/badge/Algorithms-DAA-orange" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Enabled-green" />
  <img src="https://img.shields.io/badge/Status-Development-yellow" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" />
</p>

---

## ✪ Project Overview

ProjectWise is an intelligent decision-support platform designed to help tourists make **safe, cost-effective, and informed travel decisions**.

The system integrates **graph algorithms, optimization techniques, and machine learning models** to solve real-world travel problems such as overpricing, unsafe routes, and inefficient budget planning.

Instead of relying on static recommendations, ProjectWise dynamically evaluates **cost, safety, and user constraints** to generate adaptive and personalized travel guidance.

---

## ✪ Problem Statement

Tourists often struggle with:

- Overpriced services and hidden charges  
- Unsafe or unreliable transport routes  
- Poor budget allocation during trips  
- Lack of awareness about high-risk or scam-prone areas  


---

## ✪ Solution

ProjectWise provides features such as:

- Estimates **fair prices** for transport and services  
- Recommends **safe and efficient routes**  
- Optimizes **budget allocation across activities**  
- Detects **scam-prone areas and abnormal pricing patterns**  
- Suggests **places and activities within budget constraints**  

---

## ✪ System Architecture

At the core of the system is a **Decision Engine** that integrates multiple modules:

- Algorithmic Optimization Layer  
- Machine Learning Intelligence Layer  
- Risk Analysis Engine  
- Budget Planning System  

These modules work together to deliver **real-time, data-driven recommendations**.

---

## ✪ Core Modules

### 1. Price Intelligence Module
- Regression models for fair price estimation  
- Anomaly detection for identifying overpricing  
- Classification models for scam detection  

---

### 2. Transport & Routing Module
- Graph-based modeling of transport networks  
- Shortest & safest path computation using:
  - Dijkstra Algorithm  
  - A* Search  
- Priority queue-based ranking of routes  

---

### 3. Risk Analysis Module
- Clustering techniques to identify high-risk zones  
- Graph traversal for area-wise risk scoring  
- Real-time alert ranking  

---

### 4. Budget Optimization Module
- Dynamic Programming for optimal spending  
- Greedy strategies for quick decision making  
- Knapsack-based selection of activities  

---

### 5. Recommendation Engine
- Suggests places and activities  
- Works under budget constraints  
- Balances cost, popularity, and safety  

---

## ✪ Tools & Technologies

- **Languages:** C++ / Python
- **Algorithms:** Graphs, DP, Greedy, Priority Queues
- **Machine Learning:** Scikit-learn, NumPy, Pandas  
- **Visualization:** Matplotlib  
- **Version Control:** Git & GitHub  

---

## 📁 Project Structure

```bash
projectwise/
│── data/                  # datasets
│── algorithms/
│   ├── graph/
│   ├── dp/
│   ├── greedy/
│── ml/
│   ├── regression/
│   ├── classification/
│── core/                  # main decision engine
│── utils/                 # helper functions
│── main.py                # entry point
│── requirements.txt
│── README.md
