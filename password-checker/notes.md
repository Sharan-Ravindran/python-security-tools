# 📝 Notes — Password Strength Checker

Personal notes written while building this tool. These are for my own reference.

---

## Concepts I learned

### re module (regex)
- `import re` gives you pattern matching tools
- `re.search(pattern, string)` returns a match object if found, or None if not
- Always wrap pattern in `r''` (raw string) to avoid backslash issues

```python
import re
re.search(r'[A-Z]', "Hello")   # finds uppercase — returns match
re.search(r'[A-Z]', "hello")   # no uppercase — returns None
```

Common character class patterns:
```
[A-Z]           uppercase letters
[a-z]           lowercase letters
[0-9]           digits
[!@#$%^&*]      special characters (you define which ones)
```

---

### How the scoring works
- Each check adds points to a score variable
- The total score maps to a label using a dictionary
- `.get(score, "Very Strong")` handles any score above the max gracefully

```python
levels = {0:"Very Weak", 1:"Weak", 2:"Weak", 3:"Moderate", ...}
levels.get(score, "Very Strong")
# if score is 8 (above the dict), returns "Very Strong" instead of crashing
```

---

### Dictionary `.get()` method
- Safe way to look up a key that might not exist
- Second argument is the default value if key is not found
- Never crashes unlike `dict[key]` which throws KeyError

```python
# This crashes if key missing:
my_dict[99]         # KeyError

# This is safe:
my_dict.get(99, "default")   # returns "default" instead
```

---

### `join()` for combining lists
- Turns a list of strings into one string
- Format: `"separator".join(list)`

```python
tips = ["Add uppercase", "Add numbers", "Too short"]
print(", ".join(tips))
# Output: Add uppercase, Add numbers, Too short
```

---

## Things I got wrong first time
- Forgot `r''` on regex pattern — backslashes caused issues
- Used `dict[key]` instead of `dict.get()` — crashed when score was above max
- Forgot to `import re` at the top

---

## Connection to my internship work
During the OWASP Juice Shop assessment I found that the app had no password complexity enforcement — users could set single character passwords. This tool shows I understand why that's a vulnerability and how to check for it programmatically.

---

## Resources that helped
- Python docs: `re` module — docs.python.org/3/library/re.html
- OWASP password guidelines — owasp.org/www-community/password-special-characters
