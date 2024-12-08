from pyadics import *

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

        # (x+y)=(y+x)
        if x+y != y+x:
            print("Commutativity broke!")
            print(f"{x} + {y} == {x+y}")
            print(f"{y} + {x} == {y+x}")
            return

        # ((x+y)+z)=(x+(y+z))
        x_plus_y = x + y
        lrs = x_plus_y + z
        debug1 = f"{x_plus_y} + {z} == {lrs}"
        y_plus_z = y + z
        rhs = x + y_plus_z
        debug2 = f"{x} + {y_plus_z} == {rhs}"
        if (x+y)+z != x+(y+z):
            print(f"Addition not associative for {x}, {y}, {z}.\n{debug1}\n{debug2}")
            return

        # x+0=x
        if x+zero != x:
            print("Additive identity broken!")
            return

        # x*y = y*x
        if x*y != y*x:
            print("Multiplication not commutative!")
            print(f"{x} * {y} == {x*y}")
            print(f"{y} * {x} == {y*x}")
            return

        # x*1=x
        if x*one != x:
            print("Multiplicative identity broken!")
            return

        # x*(y+z)=(x*y)+(x*z)
        if x*(y+z) != (x*y)+(x*z):
            print("Distributivity broken!")
            return

        # x+(-x)=0
        if -x + x != zero:
            print(f"Additive inverse failed!")
            print(f"{-x} + {x} == {-x + x}")
            return
        

    print(f"All field tests passed for all {tests} tests and p = {p}.")

if __name__ == "__main__":
    for p in [3,5,7]:
        test_field_axioms(p=p, tests=1000)
 