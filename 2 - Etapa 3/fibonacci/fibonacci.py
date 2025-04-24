class Fibonacci:
    def calculate(n: int):
        if not isinstance(n, int) or n < 0:
            raise ValueError("O número deve ser um inteiro não negativo.")
        
        if n == 0:
            return 0
        
        elif n == 1:
            return 1
        
        a, b = 0, 1
        
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
