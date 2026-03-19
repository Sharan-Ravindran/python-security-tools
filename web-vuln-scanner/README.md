# 🕷️ Web Vulnerability Scanner

A Python tool that scans a target web application for common vulnerabilities — specifically Cross-Site Scripting (XSS) and SQL Injection (SQLi). These are two of the OWASP Top 10 vulnerabilities.

This was built directly from my internship experience — during my OWASP Juice Shop security assessment and web application pentest, I found XSS and SQLi manually. This tool automates the detection step.

---

## What it checks for

### Cross-Site Scripting (XSS)
Injects JavaScript payloads into URL parameters and form fields. If the payload is reflected back in the response without being sanitised, the endpoint is potentially vulnerable.

### SQL Injection (SQLi)
Injects SQL characters and keywords into URL parameters. Looks for database error messages in the response — a common indicator of unsanitised SQL queries.

---

## How to run

```bash
pip install requests
python web_vuln_scanner.py
```

Enter a target URL when prompted. Only test on targets you own or have permission to test.

---

## Example output

```
============================================================
         WEB VULNERABILITY SCANNER
         For educational and authorised testing only
============================================================

Enter target URL: http://localhost/dvwa/
Starting scan of: http://localhost/dvwa/

[*] Crawling for links and forms...
[*] Found 4 URLs to test

[!] XSS FOUND     → http://localhost/dvwa/search?q=<script>alert(1)</script>
[!] SQLi FOUND    → http://localhost/dvwa/user?id=1'
[-] Clean         → http://localhost/dvwa/about
[-] Clean         → http://localhost/dvwa/login

============================================================
Scan complete
XSS vulnerabilities  : 1
SQLi vulnerabilities : 1
Clean URLs           : 2
============================================================
```

---

## Safe targets for testing

| Target | Notes |
|--------|-------|
| OWASP Juice Shop | Deliberately vulnerable — `http://localhost:3000` |
| DVWA | Damn Vulnerable Web App — run in Docker |
| OWASP BWA | Used in my internship project |
| Your own web app | Always fine |

**Never run this against a website you don't own.** Even passive scanning can be considered unauthorised access.

---

## What I learned building this

- How the `requests` library sends HTTP GET and POST requests in Python
- How XSS works at the HTTP level — injecting into parameters, reflected in response body
- How SQLi errors look in HTTP responses — error strings that leak database info
- How web crawling works — extracting links from HTML with `re` or `BeautifulSoup`
- How forms work in HTML — finding input fields and submitting test payloads
- Why input sanitisation and parameterised queries prevent these vulnerabilities

---

## Limitations

This is a basic scanner — it detects reflected XSS and error-based SQLi only. It does not detect:
- Stored XSS (payload saved in database, appears on different page)
- DOM-based XSS (happens in JavaScript, not in server response)
- Blind SQLi (no error message shown, but query still affected)
- Time-based SQLi

Professional tools like Burp Suite handle all of these. This tool is for learning how the detection logic works.

---

## Connection to internship work

During my OWASP Juice Shop assessment I found XSS and SQL injection manually — entering payloads by hand and checking responses. This tool automates exactly that process. Building it helped me understand why Burp Suite's scanner works the way it does, and gave me a much deeper understanding of what I was doing during my manual testing.

---

## Concepts used

| Concept | Purpose |
|---------|---------|
| `requests.get()` | Send HTTP GET request |
| `requests.post()` | Send HTTP POST request |
| `response.text` | Read the HTML response body |
| `re.findall()` | Extract links and form fields from HTML |
| String `in` operator | Check if error string appears in response |
| Functions | Separate logic for XSS check, SQLi check, crawling |
| Lists | Store found URLs and vulnerabilities |
