import numpy as np
import skfuzzy as fuzz
from config import *
class FuzzySets:

    def __init__(self):

        self.x_hr = np.arange(0, 241, 1)
        self.x_rr = np.arange(0, 62, 1)
        self.x_spo2 = np.arange(50, 101, 1)
        #conjunto de espera continuo con un rango de 0 a infinito
        self.x_wait = np.arange(0, 900, 1)

        # HR
        self.hr_low = fuzz.trimf(self.x_hr, [0, 30, 60])
        self.hr_mid = fuzz.trimf(self.x_hr, [50, 80, 110])
        self.hr_high = fuzz.trapmf(self.x_hr, [100, 130, 200, 240])

        # RR
        self.rr_low = fuzz.trimf(self.x_rr, [0, 6, 12.5])
        self.rr_mid = fuzz.trimf(self.x_rr, [11.5, 13, 16.5])
        self.rr_high = fuzz.trapmf(self.x_rr, [15, 17, 55, 61])

        # SpO2
        self.sp_low = fuzz.trimf(self.x_spo2, [50, 80, 92])
        self.sp_mid = fuzz.trimf(self.x_spo2, [91, 93, 94.5])
        self.sp_high = fuzz.trimf(self.x_spo2, [94, 97, 100])

        # WAIT
        self.w_low = fuzz.trimf(self.x_wait, [0, 0, 5])
        self.w_mid = fuzz.trimf(self.x_wait, [4, 6, 10])
        self.w_high = fuzz.trapmf(self.x_wait, [9, 15, 120, 120])

        # OUTPUT
        self.x_out = np.arange(0, 11, 1)
        self.out_low = fuzz.trimf(self.x_out, [0, 2, 4])
        self.out_mid = fuzz.trimf(self.x_out, [3, 5, 7])
        self.out_high = fuzz.trimf(self.x_out, [6, 8, 10])