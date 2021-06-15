import re
 
# Make a regular expression
# for validating an Email
regex = '[^@]+@[^@]+\.[^@]+'
 
# Define a function for
# for validating an Email
 
 
def check(email):
    # pass the regular expression
    # and the string in search() method
    if(re.match(regex, email)):
        print("Valid Email")
    
    else:
        print("Invalid Email")
        
        
        
email = "my.ownsite"
check(email)
