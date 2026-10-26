"""Complete the four functions. Return results; do not use input().

Keep names and parameters unchanged. No imports are needed.
"""


# 1. Conditions: Use if / elif / else: below 10 → "cold", 10–25 → "warm", above 25 → "hot".
# temperature is a number; both 10 and 25 are warm.
def describe_temperature(temperature):
    if temperature < 10:
        return "cold"
    elif temperature <= 25:
        return "warm"
    else:
        return "hot"
    
print(describe_temperature(5))
print(describe_temperature(10))
print(describe_temperature(15))
print(describe_temperature(25))
print(describe_temperature(30))
  

# 2. For Loop: Use a for loop to count even positive integers from 1 through n.
# n is non-negative. Examples: 0 → 0, 5 → 2, 6 → 3.
def count_evens(n):
    count=0
    for i in range (1, n+1):
        if i % 2 ==0:
            count+=1
        return count
print(count_evens(0))
print(count_evens(5))
print(count_evens(6))



# 3. Recursion: Use recursion to return 2 raised to power n, without ** or pow().
# n is a small non-negative integer. Examples: 0 → 1, 3 → 8.
def power_of_two(n):

