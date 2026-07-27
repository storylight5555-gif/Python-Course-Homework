def calculate_power():
    print("--- Vrisha's Power Calculator ---")
    
    try:
        base = float(input("Enter the base number: "))
        exponent = float(input("Enter the power (n): "))
        
        result = base ** exponent
        
        
        if base.is_integer(): base = int(base)
        if exponent.is_integer(): exponent = int(exponent)
        if result.is_integer(): result = int(result)
            
        print(f"\nResult: {base} raised to the power of {exponent} is {result}")
        
    except ValueError:
        print("Error: Please enter valid numbers only.")

if __name__ == "__main__":
    calculate_power()
