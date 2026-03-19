# 🔑 Password Strength Checker

A Python script that analyses how strong a password is based on character diversity, length, and common pattern detection.

This was the first tool I built after my cybersecurity internship — I wanted to understand how password policies work at the code level rather than just knowing they exist.

---

## What it does

- Scores the password from 0 to 7
- Checks for uppercase letters, lowercase letters, numbers and special characters
- Flags if the password is too short
- Gives specific feedback on what to improve
- Labels strength as Very Weak / Weak / Moderate / Strong / Very Strong

---

## How to run

```bash
python password_checker.py
```

No external libraries needed — uses only Python's built-in `re` module.

---

## Example output

```
Enter password: hello
Strength: Weak
Score: 2/7
Tips: Use at least 8 characters, Add uppercase letters, Add numbers, Add special characters (!@#$%^&*)

Enter password: MyP@ssw0rd#2024
Strength: Very Strong
Score: 7/7
```

---

## What I learned building this

- How regex works in Python (`re` module)
- Why password complexity rules exist — each character class massively increases the number of possible combinations an attacker has to try
- How OWASP password guidelines are structured
- The difference between checking `if` a condition is true vs scoring it with points

---

## Concepts used

| Concept | Where it appears |
|---------|-----------------|
| `re.search()` | Checking for character classes |
| Functions | `check_password_strength()` |
| Dictionaries | Mapping scores to strength labels |
| f-strings | Formatting output |
| `join()` | Combining tips list into one line |

---

## Why this matters in cybersecurity

During my internship, one of the vulnerabilities I found was weak credentials — users with passwords like `admin123`. Understanding how password strength is measured helps in two ways: building better login systems, and understanding what makes a credential easy or hard to crack during a pentest.
