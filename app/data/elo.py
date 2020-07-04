import mpmath as mp

# mpmath init
mp.dps = 15
mp.pretty = True


# Expected scores
def exp_score(R_a, R_b):
    Q_a = mp.power(10, (R_a / 400))
    Q_b = mp.power(10, (R_b / 400))
    E_a = mp.fdiv(Q_a, sum([Q_a, Q_b]))
    E_b = mp.fdiv(Q_b, sum([Q_a, Q_b]))
    return (E_a, E_b)


# Rating updates
def up_rating(R_a, R_b, S_a, S_b):
    K = 32
    E_scores = exp_score(R_a, R_b)
    E_a = E_scores[0]
    E_b = E_scores[1]
    Rnew_a = R_a + K * (S_a - E_a)
    Rnew_b = R_b + K * (S_b - E_b)
    return (Rnew_a, Rnew_b)
