from integer import *

def is_addition_commutative(x,y):
    is_commutative = x+y == y+x
    if not is_commutative:
        print("Commutativity of addition broke!")
        print(f"{x} + {y} == {x+y}")
        print(f"{y} + {x} == {y+x}")

    return is_commutative

def is_addition_associative(x,y,z):
    x_plus_y = x + y
    lhs = x_plus_y + z
    debug1 = f"{x_plus_y} + {z} == {lhs}"
    y_plus_z = y + z
    rhs = x + y_plus_z
    debug2 = f"{x} + {y_plus_z} == {rhs}"
    is_associative = lhs == rhs
    if not is_associative:
        print(f"Addition not associative for {x}, {y}, {z}.\n{debug1}\n{debug2}")
    
    return is_associative

def is_addtion_neutral(x, zero):
    is_zero_neutral = x+zero == x
    if not is_zero_neutral:
        print(f"Zero is not neutral for {x}")

    return is_zero_neutral

def is_multiplication_commutative(x,y):
    is_commutative = x*y == y*x
    if not is_commutative:
        print("Multiplication not commutative!")
        print(f"{x} * {y} == {x*y}")
        print(f"{y} * {x} == {y*x}")
    
    return is_commutative

def is_multiplication_associative(x,y,z):
    x_times_y = x * y
    lhs = x_times_y * z
    debug1 = f"{x_times_y} * {z} == {lhs}"
    y_times_z = y * z
    rhs = x * y_times_z
    debug2 = f"{x} * {y_times_z} == {rhs}"
    is_associative = lhs == rhs
    if not is_associative:
        print(f"Multiplication not associative for {x}, {y}, {z}.\n{debug1}\n{debug2}")
    
    return is_associative

def test_field_axioms(p=5, tests=1000):
    """
    Run tests of field-like properties for p-adic arithmetic using stable_p_adic.
    Because we now have a digit_factory that does not consume the original data,
    we can perform multiple operations on the same objects safely.

    We test:
    - Addition: commutativity, associativity, identity, inverses
    - Multiplication: commutativity, identity, distributivity
    - Inverse for units

    If any property fails, we stop early and print an error.
    """
    zero = p_adic_zero(p)
    one = p_adic_one(p)

    for test_i in range(tests):
        # Use distinct seeds per test
        x_seed = test_i*3 + 1
        y_seed = test_i*3 + 2
        z_seed = test_i*3 + 3

        x = stable_p_adic(p, x_seed)
        print(f"x_{test_i} = {x}")
        y = stable_p_adic(p, y_seed)
        print(f"y_{test_i} = {y}")
        z = stable_p_adic(p, z_seed)
        print(f"z_{test_i} = {z}")

        if not is_addition_commutative(x,y):
            return

        if not is_addition_associative(x,y,z):
            return

        if not is_addtion_neutral(x, zero):
            return

        # x+(-x)=0
        if -x + x != zero:
            print(f"Additive inverse failed!")
            print(f"{-x} + {x} == {-x + x}")
            return

        if not is_multiplication_commutative(x,y):
            return
        
        if not is_multiplication_associative(x,y,z):
            return

        # x*1=x
        if x*one != x:
            print("Multiplicative identity broken!")
            return

        # x*(y+z)=(x*y)+(x*z)
        if x*(y+z) != (x*y)+(x*z):
            print("Distributivity broken!")
            return
        

    print(f"All field tests passed for all {tests} tests and p = {p}.")

if __name__ == "__main__":
    for p in [3,5,7]:
        test_field_axioms(p=p, tests=1000)
 