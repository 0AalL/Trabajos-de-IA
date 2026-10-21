class FuzzyRules:

    def __init__(self):

        self.rules = [

            # -------------------
            # PRIORIDAD ALTA (urgencia médica)
            # -------------------
            ("hr_high", "sp_low", "any", "level3"),
            ("rr_high", "sp_low", "any", "level3"),
            ("hr_high", "rr_high", "any", "level3"),

            # -------------------
            # PRIORIDAD ALTA POR ESPERA
            # -------------------
            ("wait_high", "any", "any", "level3"),

            # -------------------
            # BALANCE (espera + condición media)
            # -------------------
            ("hr_mid", "rr_mid", "sp_mid", "level2"),
            ("hr_mid", "rr_high", "sp_mid", "level2"),
            ("hr_low", "rr_mid", "sp_low", "level2"),

            ("wait_mid", "any", "any", "level2"),

            # -------------------
            # BAJA PRIORIDAD
            # -------------------
            ("hr_low", "rr_low", "sp_high", "level1"),
            ("hr_low", "sp_high", "any", "level1"),
            ("rr_low", "sp_high", "any", "level1"),
        ]