import re
import math
def password_strength(password):
    score=0
    feedback=[]
    if len(password)>=12:
        score+=2
    elif len(password)>=8:
        score+=1
    else:
        feedback.append("use atleast 8 characters \n")
    if re.search(r"[A-Z]",password):
        score+=1
    else:
        feedback.append("use atleast 1 uppercase letter \n")
    if re.search(r"[a-z]",password):
        score+=1
    else:
        feedback.append("use atleast 1 lowercase letter \n")
    if re.search(r"[0-9]",password):
        score+=1
    else:
        feedback.append("use atleast 1 number \n")
    if re.search(r"[!@#$%^&*]",password):
        score+=2
    else:
        feedback.append("use atleast 1 special character(!@#$%^&*)\n")
    levels={0:"very weak",1:"weak",2:"weak",3:"moderate",4:"moderate",5:"strong",6:"strong",7:"super strong"}
    print(f"Strength: {levels.get(score, 'super strong')}")
    print(f"Score: {score}/7")
    if feedback:
        print("Tips:", ", ".join(feedback))
        
    
print("\t\t\n PASSWORD STRENGTH CHECKER")
password=input("Enter the password to check:")
password_strength(password)
