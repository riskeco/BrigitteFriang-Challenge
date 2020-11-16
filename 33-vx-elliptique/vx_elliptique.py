
# Constants

n = 57896044618658097711785492504343953926634992332820282019728792003956564819949
x = 54387532345611522562080964454373961410727797296305781726528152669705763479709
y = 14361142164866602439359111189873751719750924094051390005776268461061669568849

y1 = 43534902453791495272426381314470202206884068238768892013952523542894895251100
y2 = 30324056046686065827439799532301040739788176334375034006985657438931650257514

print("Constants :")
print("n  =",n)
print("x  =",x)
print("y  =",y)
print("y1 =",y1)
print("y2 =",y2)

# Find A such that (E) is satisfied
# (E) : y^2 = x^3 + Ax^2 + x [n]
# so such that Ax^2 = y^2 - x^3 - x [n]
# We need to invert x^2 in Z/nZ

A = pow(x*x, -1, n)*(y*y - x*x*x - x)%n
# A = 486662

print("\nElliptic curve :")
print("A  =",A)
# We now have the complete definition of the elliptic curve

# The next step is to find x1 and x2 such that k1 = (x1, y1), k2 = (x2, y2) are valid points on the curve
# ie to solve the equation x^3 + Ax^2 + x - B = 0 [n] (where B is knwn B=y^2)
# This is a problem of factoring a polynomial in Z/nZ

from sympy import poly, ground_roots
from sympy.abc import x

f_x1 = poly(x**3+A*x*x+x-(y1*y1)%n, modulus=n)

roots_x1 = ground_roots(f_x1, modulus=n)

roots_list_x1 = list(roots_x1.keys())
u = roots_list_x1[0]%n
v = roots_list_x1[1]%n
w = roots_list_x1[2]%n

print("\nRoots for x1 :")
print("u  =",u)
print("v  =",v)
print("w  =",w)

f_x2 = poly(x**3+A*x*x+x-(y2*y2)%n, modulus=n)

roots_x2 = ground_roots(f_x2, modulus=n)

# only one possible value for x2
x2 = list(roots_x2.keys())[0]

print("\nRoot for x2 :")
print("x2  =", x2)

# we have n + (n-1)/2*(-2) = 1
# multiplying that by (x2 - x1) gives
# k * n + k2 * (n-1)/2 = (x2 - x1)

a  = x2 - u
# k2 = -2*(x2-u)

z = (u + a*n)%(n*(n-1)//2)

print("\nSolution for z :")
print("z  =",z)
