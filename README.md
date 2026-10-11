# OT-Research
---

# Covert Channels, C2, and ML-Based Detection of CTC

This project explores **covert post-exploitation techniques** and proposes a **machine learning-based approach** for detecting **Covert Timing Channels (CTCs)**. It combines offensive and defensive cybersecurity practices in a practical, research-driven setting.

## Project Structure

### 1. **Post-Exploitation & Covert C2 Channel**

* Exploits `CVE-2020-2555` on Oracle Coherence via Metasploit.
* Deploys a custom C2 agent (`VSAgent`) that abuses the `__VIEWSTATE` parameter in HTTP to send/receive commands.
* C2 server mimics legitimate ASP.NET traffic to evade detection.

### 2. **Detection of Covert Timing Channels (CTCs)**

* Captures network traffic and converts it into image-like features.
* Trains ML models (Decision Tree, ANN, SVM) to classify traffic as **normal** or **covert**.
* Uses 16×16 IAT-based image matrices and statistical feature extraction.

## Key Insights

* **Decision Tree** achieved 100% detection of covert traffic.
* **ANN and SVM** models failed to detect covert traffic due to class imbalance (only 3 covert samples in test set).


##  Contents

* Covert C2 Setup with VSAgent – https://github.com/Joellots/VSAgent
* `extract_iats` – Script for extracting Inter-Arrival Time (IAT) from Packet Captures.
* `iat_to_images` – Script for flow image generation from Inter-Arrival Time (IAT).
* `Model_Analysis` – Jupyter Notebook containing flow image creation, Feature extraction, EDA, ML classification training. and Visualization of generated flow images
* `packet-captures/` – Wireshark pcap files and flow inspection images.
* `iat_images/` – Pipeline diagrams, ML metrics, and screenshots of covert traffic and agent interaction.
* `models/` – Trained Machine Learning Models.

  
## Tools Used

* **Metasploit**, **Nmap**, **Wireshark**, **Python**, **Scikit-learn**, **Matplotlib**, **NumPy**, **Pandas**

## Author

**Okore Joel Chidike**, 
Security and Network Engineering (SNE), M24-SNE-01
Innopolis University

