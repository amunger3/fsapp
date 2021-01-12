import mpmath as mp

# mpmath init
mp.dps = 15
mp.pretty = True


class Elo:

    def __init__(self, R_tup=(1500, 1500), S_tup=(0.5, 0.5)):
        self.K = 32
        self.R_tup = R_tup
        self.S_tup = S_tup
        self.Q_tup = tuple(map(lambda x: mp.power(10, (x / 400)), self.R_tup))
        self.E_tup = tuple(mp.fdiv(Q_ab, sum(self.Q_tup)) for Q_ab in self.Q_tup)
        self.Rnew = tuple(self.R_tup[i] + self.K * (self.S_tup[i] - self.E_tup[i]) for i in range(2))
