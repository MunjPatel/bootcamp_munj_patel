import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class CleanData:

    @staticmethod

    def fill_missing_median(data_frame):
        data = data_frame.fillna(data_frame.median(numeric_only=True))
        return data
    
    @staticmethod
    def drop_missing(data_frame):
        data = data_frame.dropna(how = 'any').reset_index(drop = True)
        return data
    
    @staticmethod
    def normalize_data(data_frame):
        # Assuming your DataFrame is named data_frame
        data_frame = data_frame.select_dtypes(include=np.number)
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data_frame)
        return scaled_data
    
