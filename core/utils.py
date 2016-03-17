import math

def normalize(floats, floats_sum=None):
    if floats_sum is None:
        floats_sum = 0.0
        for i in range(len(floats)):
            floats_sum += floats[i]
    if math.isnan(floats_sum):
        raise ValueError("Can't normalize list. Sum is NaN.")
    if floats_sum is 0:
        raise ValueError("Can't normalize list. Sum is zero.")
    for i in range(len(floats)):
        floats[i] /= floats_sum

def compare(f1, f2):
    """Compare two float values.
    """
    if f1 < f2:
        return -1
    if f1 > f2:
        return 1
    # Values are equal
    return 0

def normal_probability(a):
    x = a * 7.07106781186547524401e-1
    y = 0.5
    z = math.abs(x)

    if z < 7.07106781186547524401e-1:
        y += 0.5 * error_function(x)
    else:
        y *= error_function_complemented(z)
        if x > 0:
            y = 1.0 - y
    return y

def error_function(x):
    T = [9.60497373987051638749E0, 
    9.00260197203842689217E1, 
    2.23200534594684319226E3, 
    7.00332514112805075473E3,
    5.55923013010394962768E4]
    
    U = [3.35617141647503099647E1,
    5.21357949780152679795E2,
    4.59432382970980127987E3,
    2.26290000613890934246E4,
    4.92673942608635921086E4]

    if math.abs(x) > 1.0:
        return 1.0 - error_function_complemented(x)

    z = x * x
    y = x * polevl(z, T, 4) / p1evl(z, U, 5)
    return y

def error_function_complemented(a):
    P = [2.46196981473530512524E-10,
    5.64189564831068821977E-1,
    7.46321056442269912687E0,
    4.86371970985681366614E1,
    1.96520832956077098242E2,
    5.26445194995477358631E2,
    9.34528527171957607540E2,
    1.02755188689515710272E3,
    5.57535335369399327526E2]

    Q = [1.32281951154744992508E1,
    8.67072140885989742329E1,
    3.54937778887819891062E2,
    9.75708501743205489753E2,
    1.82390916687909736289E3,
    2.24633760818710981792E3,
    1.65666309194161350182E3,
    5.57535340817727675546E2]
  
    R = [5.64189583547755073984E-1,
    1.27536670759978104416E0,
    5.01905042251180477414E0,
    6.16021097993053585195E0,
    7.40974269950448939160E0,
    2.97886665372100240670E0]

    S = [2.26052863220117276590E0,
    9.39603524938001434673E0,
    1.20489539808096656605E1,
    1.70814450747565897222E1,
    9.60896809063285878198E0,
    3.36907645100081516050E0]

    if a < 0:
        x = -a
    else:
        x = a

    if x < 1:
        return 1.0 - error_function(a)

    z = -a * a

    if z < -7.09782712893383996732e2:
        if a < 0:
            return 2.0
        else:
            return 0.0

    z = math.exp(z)

    if x < 8:
        p = polevl(x, P, 8)
        q = p1evl(x, Q, 8)
    else:
        p = polevl(x, R, 5)
        q = p1evl(x, S, 6)

    y = (z * p) / q

    if a < 0:
        y = 2.0 - y

    if y == 0:
        if a < 0:
            return 2.0
        else:
            return 0.0
    return y

def polevl(x, coef, N):
    ans = coef[0]
    for i in range(1, N + 1):
        ans = ans * x + coef[i]
    return ans

def p1evl(x, coef, N):
    ans = x + coef[0]
    for i in range(1, N):
        ans = ans * x + coef[i]
    return ans

def is_missing_value(val):
    return math.isnan(val)

def log2(a):
    return math.log(a) / math.log(2)

def eq(a, b):
    # Small deviation allowed in comparisons
    allowed_deviation = 1e-6
    return a is b or ((a - b < allowed_deviation) and (b - a < allowed_deviation))

def entropy(array):
    return_value = 0
    sum_value = 0

    for i in range(len(array)):
        return_value -= ln_func(array[i])
        sum_value += array[i]
    if eq(sum_value, 0):
        return 0
    else:
        return (return_value + ln_func(sum_value)) / (sum_value * math.log(2))

def ln_func(num):
    if num <= 0:
        return 0
    else:
        return num * math.log(num)