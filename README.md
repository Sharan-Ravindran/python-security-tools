
# 🔐 Python Security Tools

A collection of cybersecurity tools built in Python as part of my learning journey after completing a cybersecurity internship at **Innoknowvex**.

Each tool was built from scratch to understand the underlying concepts — not copied. The `basic/` and `advanced/` versions in each folder show my progression.

```

## 📁 Repository Structure
---
python-security-tools/
│
├── password-checker/
│   ├── password_checker.py       ← single file, beginner friendly
│   └── notes.md                  ← what I learned building this
│
├── port-scanner/
│   ├── basic/
│   │   └── port_scanner.py       ← single threaded version
│   ├── advanced/
│   │   └── port_scanner_threaded.py  ← multithreaded version
│   └── notes.md                  ← what I learned building this
│
├── web-vuln-scanner/
│   ├── web_vuln_scanner.py       ← XSS and SQLi detection
│   └── notes.md                  ← what I learned building this
│
└── README.md                     ← this file
```

## 🛠️ Tools Overview

| Tool | Concepts | Difficulty |
|------|----------|------------|
| Password Checker | Regex, string analysis, OWASP password guidelines | Beginner |
| Port Scanner (basic) | TCP sockets, networking fundamentals | Beginner |
| Port Scanner (threaded) | Multithreading, Queue, thread safety | Intermediate |
| Web Vuln Scanner | HTTP requests, XSS, SQLi detection | Intermediate |

---

## ⚙️ Requirements

- Python 3.x
- `requests` library (for web vuln scanner only)

Install requests:
```
pip install requests
```

---

## ▶️ How to Run Each Tool

```bash
# Password checker
python password-checker/password_checker.py

# Port scanner basic
python port-scanner/basic/port_scanner.py

# Port scanner threaded
python port-scanner/advanced/port_scanner_threaded.py

# Web vulnerability scanner
python web-vuln-scanner/web_vuln_scanner.py
```

---

## ⚠️ Legal Notice

These tools are built for **educational purposes only**.

Only use them on systems you own or have explicit written permission to test. Unauthorised scanning or testing of systems is illegal under the Computer Fraud and Abuse Act (CFAA) and equivalent laws worldwide.

The author takes no responsibility for misuse of these tools.

---

## 👤 About

Built by **Sharan Ravindran**
Cybersecurity Intern @ Innoknowvex

- 🔗 LinkedIn: www.linkedin.com/in/sharan-ravindran-83b4b3361
- 📧 Email: uwitkuwit@gmail.com

---

## 📚 Background

These tools were built after completing:
- End-to-end web application penetration testing (major internship project)
- Security assessment of OWASP Juice Shop (minor internship project)
- TryHackMe Cybersecurity 101 path (in progress)
