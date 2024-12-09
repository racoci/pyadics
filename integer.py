"""
This module demonstrates a p-adic arithmetic model without consuming the original
digit generators. Instead, each Integer_P_Adic holds a 'digit_factory' that can produce a fresh
identical infinite generator of digits each time it is called. This allows us to
perform multiple operations on the same Integer_P_Adic number without losing the original data.

We test field axioms and properties similar to before, but now we ensure reproducibility
and no unwanted consumption of generators.
"""

import random
from math import gcd
import itertools

DEFAULT_PRIME_BASE = 3
DEFAULT_MAX_P_GITS = 20

def stable_p_adic(p=DEFAULT_PRIME_BASE, seed=None):
    """
    Create a stable p-adic number. We generate 'length' digits first and then yield zeros.
    A factory function returns this same sequence every time it's called, allowing
    for infinite cloning without consumption issues.
    """

    def digit_factory():
        def gen():
            rng = random.Random(seed)
            while True:
                d = rng.randint(0, p-1)
                yield d
        return gen()
    return Integer_P_Adic(p, digit_factory)

def p_adic_equal(x, y, num_digits=DEFAULT_MAX_P_GITS):
    """
    Compare the first num_digits of x and y for equality by fetching fresh generators.
    """
    xg = x.digit_factory()
    yg = y.digit_factory()
    combined = itertools.zip_longest(xg, yg, fillvalue=0)
    for _ in range(num_digits):
        try:
            dx,dy = next(combined)
        except:
            return True
        else:
            if dx != dy:
                return False
    
    return True

def p_adic_zero(p=DEFAULT_PRIME_BASE):
    def digit_factory():
        def gen():
            yield 0
        return gen()
    return Integer_P_Adic(p, digit_factory)

def p_adic_one(p=DEFAULT_PRIME_BASE):
    def digit_factory():
        def gen():
            yield 1
        return gen()
    return Integer_P_Adic(p, digit_factory)

def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm.
    Returns (g, x, y) such that a*x + b*y = g = gcd(a,b).
    """
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        return (g, y1, x1 - (a // b)*y1)

def mod_inverse(x, p=DEFAULT_PRIME_BASE):
    """
    Compute inverse of x modulo p using extended Euclidean algorithm.
    """
    g, a, b = extended_gcd(x, p)
    if g != 1:
        raise ValueError("No inverse, not coprime.")
    return a % p

def p_adic_from_integer(n: int, p=DEFAULT_PRIME_BASE):
    def number_generator():
        def gen():
            r = n
            while r > 0:
                yield r % p
                r = r // p

        return gen()

    return Integer_P_Adic(p, number_generator)

class Integer_P_Adic:
    """
    A p-adic number represented by a digit_factory that can produce identical
    digit sequences each time it's called.

    We implement __add__, __mul__, and __str__.

    The __str__ prints some leading digits in reverse order to mimic a p-adic style like "...3210".
    """
    def __init__(self, p, digit_factory):
        self.p = p
        self.digit_factory = digit_factory  # A callable returning a fresh generator

    def copy(self):
        copies = itertools.tee(self.digit_factory(), 1)
        xg = copies[0]
        p = self.p
        def copy_generator():
            def gen():
                for x in xg:
                    yield x
            
            return gen()
                    
        return Integer_P_Adic(p, copy_generator)

    def __str__(self):
        # Show 20 digits for representation:
        #digits = [str(x) for x in list(itertools.islice(self.digit_factory(), 20))]
        digits = []
        prefix = ""
        try:
            for n, x in enumerate(self.digit_factory()):
                if n > DEFAULT_MAX_P_GITS:
                    prefix = "..."
                    break
                digits.append(str(x))
        except:
            prefix = ""

        return prefix + "".join(digits[::-1]) + f" (base {self.p})"

    def __lshift__(self, n):
        # self << n
        if n < 0:
            return self >> (-n)
        
        if n == 0:
            return self
        
        xg = self.digit_factory()
        p = self.p

        def left_shift_factory():
            def gen():
                for _ in range(n):
                    yield 0
                
                for x in xg:
                    yield x
                
            return gen()

        return Integer_P_Adic(p, left_shift_factory)
        
    def __rshift__(self, n):
        # self >> n
        if n < 0:
            return self << (-n)
        
        xg = self.digit_factory()
        p = self.p
        

        def right_shift_factory():
            def gen():
                m = n
                for x in xg:
                    if m > 0:
                        m -= 1
                    else:
                        yield x
                
                yield 0
                
            return gen()

        return Integer_P_Adic(p, right_shift_factory)
    
    def __add__(self, other):
        if self.p != other.p:
            raise ValueError("Cannot add p-adics with different primes.")

        p = self.p
        xg = self.digit_factory()
        yg = other.digit_factory()

        def sum_factory():
            carry = 0
            def gen():
                for dx, dy in itertools.zip_longest(xg, yg, fillvalue=0):
                    s = dx + dy + carry
                    digit = s % p
                    carry = s // p
                    yield digit
            
            return gen()
    
        return Integer_P_Adic(p, sum_factory)
    
    def __radd__(self, other):
        if self.p != other.p:
            raise ValueError("Cannot add p-adics with different primes.")

        p = self.p
        xg = self.digit_factory()
        yg = other.digit_factory()

        def sum_factory():
            def gen():
                carry = 0
                for dx, dy in itertools.zip_longest(xg, yg, fillvalue=0):
                    s = dx + dy + carry
                    digit = s % p
                    carry = s // p
                    yield digit
                    
            return gen()

        self.digit_factory = sum_factory

    def __mul__(self, other):
        p = self.p
        
        if isinstance(other, int):
            if other == 0:
                return p_adic_zero(p)
            if other < 0:
                return (-self) * (-other)
            if other > p:
                return self * p_adic_from_integer(other, p)
            
            xg = self.digit_factory()

            def prod_factory():
                def gen():
                    carry = 0
                    for x in xg:
                        s = carry + x * other
                        digit = s % p
                        carry = s // p
                        yield digit
                return gen()

            return Integer_P_Adic(self.p, prod_factory)
        
        if isinstance(other, Integer_P_Adic):
            if self.p != other.p:
                raise ValueError("Cannot multiply p-adics with different primes.")
            
            def product_factory():
                def gen():
                    # c_{-1}=0
                    carry = 0
                    # We'll produce digits d_k for k = 0,1,2,...
                    x_digits = []
                    y_digits = []
                    # For each k, we need x_0..x_k and y_0..y_k
                    k = 0
                    while True:
                        # Ensure we have at least k+1 digits from each
                        while len(x_digits) <= k:
                            try:
                                x_digits.append(next(xg))
                            except StopIteration:
                                # If x digits end, we can still proceed if infinite zeros are implied
                                x_digits.append(0)

                        while len(y_digits) <= k:
                            try:
                                y_digits.append(next(yg))
                            except StopIteration:
                                # If y digits end, append zeros
                                y_digits.append(0)

                        # Compute t_k
                        # t_k = carry + sum_{ℓ=0}^{k} x_ℓ y_{k-ℓ}
                        # Let's do a simple sum:
                        t_k = carry
                        # sum pairs: 
                        # We'll sum over ℓ=0..k: x_ℓ * y_{k-ℓ}
                        # This is O(k) per step:
                        partial_sum = 0
                        for ℓ in range(k+1):
                            partial_sum += x_digits[ℓ] * y_digits[k - ℓ]
                        t_k += partial_sum

                        # d_k and new carry
                        d_k = t_k % p
                        carry = t_k // p

                        yield d_k
                        k += 1

                return gen()

            return Integer_P_Adic(p, product_factory)
        

        raise ValueError(f"Cannot multiply PAddic number by {type(other)}")

    def __invert__(self):
        p = self.p
        def digit_factory():
            # For negation, we read from x a fresh generator and negate each digit
            base_g = self.digit_factory()
            def gen():
                for d in base_g:
                    yield p - d - 1
            return gen()
        return Integer_P_Adic(p, digit_factory)
    
    def __eq__(self, other):
        return p_adic_equal(self, other)
    
    def __ne__(self, other):
        return not p_adic_equal(self, other, 1000)

    def __neg__(self):
        return ~self + p_adic_one(self.p)
    
    def to_base(q: int):
        p = self.p
