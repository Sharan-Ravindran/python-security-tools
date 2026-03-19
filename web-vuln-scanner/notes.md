# 📝 Notes — Web Vulnerability Scanner

Personal notes written while building this tool. Connects directly to what I did manually during my internship.

---

## Core concepts

### What is XSS (Cross-Site Scripting)?

A vulnerability where an attacker can inject JavaScript into a web page that runs in another user's browser.

How it happens:
```
User input:   <script>alert('hacked')</script>
App stores/reflects it without sanitising
Browser sees: <script>alert('hacked')</script>
Browser runs: the JavaScript — popup appears (or worse, steals cookies)
```

Three types:
- **Reflected XSS** — payload in URL, reflected immediately in response. What this scanner detects.
- **Stored XSS** — payload saved in database, affects everyone who views that page. Harder to detect automatically.
- **DOM-based XSS** — payload processed by JavaScript in the browser. Not detectable by reading server responses.

Common XSS test payloads:
```
<script>alert(1)</script>
<img src=x onerror=alert(1)>
"><script>alert(1)</script>
```

How to detect reflected XSS in code:
```python
payload = "<script>alert('xss')</script>"
response = requests.get(url + payload)
if payload in response.text:
    print("Potentially vulnerable to XSS")
```

---

### What is SQL Injection?

A vulnerability where user input gets inserted directly into a SQL query without sanitisation.

How it happens:
```python
# Vulnerable code (never do this):
query = "SELECT * FROM users WHERE id = " + user_input

# Attacker enters: 1' OR '1'='1
# Query becomes:  SELECT * FROM users WHERE id = 1' OR '1'='1
# This returns ALL users instead of just id=1
```

Common SQLi test payloads:
```
'
1'
1 OR 1=1
' OR '1'='1
```

Error-based detection — look for these strings in the response:
```
sql syntax
mysql_fetch
ORA-01756
Microsoft OLE DB
SQLite3::
PostgreSQL
Warning: pg_
```

If any of these appear after injecting `'` into a parameter, the app is likely vulnerable.

---

## requests library

```python
import requests

# GET request (like typing URL in browser)
response = requests.get("http://example.com/page?id=1")

# POST request (like submitting a form)
data = {"username": "admin", "password": "test"}
response = requests.post("http://example.com/login", data=data)

# Useful response attributes:
response.text         # HTML content as string
response.status_code  # 200 = OK, 404 = not found, 500 = server error
response.url          # final URL after redirects
response.headers      # HTTP headers dict
```

---

## Extracting links from HTML

Simple way using regex:

```python
import re

html = response.text
links = re.findall(r'href=["\'](.*?)["\']', html)
```

More complete way using BeautifulSoup (more reliable):

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
links = [a['href'] for a in soup.find_all('a', href=True)]
forms = soup.find_all('form')
```

---

## Extracting form fields

Forms are how web apps take input — they need to be found and tested:

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
forms = soup.find_all("form")

for form in forms:
    action = form.get("action")    # where the form submits to
    method = form.get("method", "get").lower()   # GET or POST
    inputs = form.find_all("input")
    
    for input_field in inputs:
        name = input_field.get("name")    # parameter name
        type_ = input_field.get("type")   # text, password, hidden etc.
```

---

## Why sanitisation prevents XSS

Vulnerable:
```python
output = "<p>Hello " + user_input + "</p>"
# if user_input = <script>alert(1)</script>
# output = <p>Hello <script>alert(1)</script></p>  ← runs JS
```

Fixed with HTML escaping:
```python
import html
output = "<p>Hello " + html.escape(user_input) + "</p>"
# if user_input = <script>alert(1)</script>
# output = <p>Hello &lt;script&gt;alert(1)&lt;/script&gt;</p>  ← displays as text, not code
```

---

## Why parameterised queries prevent SQLi

Vulnerable:
```python
query = "SELECT * FROM users WHERE id = " + user_input
cursor.execute(query)
```

Fixed:
```python
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_input,))   # input is treated as data, not SQL code
```

The `?` is a placeholder — the database driver handles escaping. User input can never break out of the data context.

---

## Things I got wrong first time

- Didn't handle redirects — `requests` follows them automatically which is usually fine
- Tested on URLs without query parameters — XSS/SQLi need somewhere to inject
- Didn't set a timeout on requests — scanner hung on slow/dead hosts
- Forgot to URL-encode payloads — some payloads need encoding to survive in a URL

Always add timeout to requests:
```python
response = requests.get(url, timeout=5)
```

---

## Connection to internship work

I found XSS and SQLi manually in the OWASP Juice Shop by entering payloads in the browser and checking if they were reflected. This tool does the same thing programmatically. Building it made me understand exactly what Burp Suite's active scanner is doing under the hood — it's the same logic, just more comprehensive payloads and smarter detection.

During my web application pentest (major project) I used Burp Suite's scanner — now I understand what it's doing at the code level.

---

## Resources
- OWASP XSS: owasp.org/www-community/attacks/xss
- OWASP SQLi: owasp.org/www-community/attacks/SQL_Injection
- requests library docs: docs.python-requests.org
- BeautifulSoup docs: beautiful-soup-4.readthedocs.io
