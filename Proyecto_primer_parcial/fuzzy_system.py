import numpy as np
import skfuzzy as fuzz
from fuzzy_sets import FuzzySets
from fuzzy_rules import FuzzyRules


class FuzzySystem:

    def __init__(self, genes):
        self.sets = FuzzySets()
        self.g = genes
        self.rules = FuzzyRules()

    def infer(self, hr, rr, spo2, wait):

        fs = self.sets

        # ------------------------
        # FUZZIFICACIÓN
        # ------------------------
        values = {
            "hr_low": fuzz.interp_membership(fs.x_hr, fs.hr_low, hr),
            "hr_norm": fuzz.interp_membership(fs.x_hr, fs.hr_mid, hr),
            "hr_high": fuzz.interp_membership(fs.x_hr, fs.hr_high, hr),

            "rr_low": fuzz.interp_membership(fs.x_rr, fs.rr_low, rr),
            "rr_norm": fuzz.interp_membership(fs.x_rr, fs.rr_mid, rr),
            "rr_high": fuzz.interp_membership(fs.x_rr, fs.rr_high, rr),

            "sp_low": fuzz.interp_membership(fs.x_spo2, fs.sp_low, spo2),
            "sp_mid": fuzz.interp_membership(fs.x_spo2, fs.sp_mid, spo2),
            "sp_high": fuzz.interp_membership(fs.x_spo2, fs.sp_high, spo2),

            "wait_low": fuzz.interp_membership(fs.x_wait, fs.w_low, wait),
            "wait_mid": fuzz.interp_membership(fs.x_wait, fs.w_mid, wait),
            "wait_high": fuzz.interp_membership(fs.x_wait, fs.w_high, wait),
        }

        output_map = {
            "level1": fs.out_low,
            "level2": fs.out_mid,
            "level3": fs.out_high
        }

        aggregated = np.zeros_like(fs.x_out)

        # ------------------------
        # REGLAS
        # ------------------------
        for i, (a, b, c, out) in enumerate(self.rules.rules):

            v1 = values.get(a, 1)
            v2 = values.get(b, 1)
            v3 = values.get(c, 1)

            #  activación 
            activation = max(min(v1, v2, v3), 0.2)

            # peso del genoma
            peso = self.g[i] if i < len(self.g) else 1
            activation *= peso

            rule_output = np.fmin(activation, output_map[out])

            aggregated = np.fmax(aggregated, rule_output)

        # ------------------------
        # DEFUZZIFICACIÓN
        # ------------------------
        result = fuzz.defuzz(fs.x_out, aggregated, "centroid")

        return  result