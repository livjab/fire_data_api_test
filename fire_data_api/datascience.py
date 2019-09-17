"""
All the DS stuff we need.
"""
# DS Logic imports
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from pandas.util.testing import assert_frame_equal

# joblib to load model
from sklearn.externals import joblib
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

# database imports
from .models import db, Fire

# the source of our live data!
modis_url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_24h.csv'


def pull_modis(url = modis_url):
    """
    Get latest modis data.
    """
    df = pd.read_csv(url, sep=',')
    return df

def process_live_data(original_df):
    """
    Pre processes live data to match pipeline expectations.
    """
    df = original_df.copy()
    #process satellite labels
    df['satellite'] = df['satellite'].replace({'T':'Terra', 'A': 'Aqua'})
    
    #process time features
    df['acq_date'] = pd.to_datetime(df['acq_date'])
    df['month'] = df['acq_date'].dt.month
    df['week'] = df['acq_date'].dt.weekofyear
    df.drop(columns=['acq_date', 'acq_time'], inplace=True)
    
    return df

def load_model(path = 'dtc_pipeline_baseline_full_v2.pkl'):
    """
    Loads our trained classification model pipeline. 
    Must define a custom FunctionTransformer method before loading trained pipeline.
    """
    return joblib.load(path)

def classify_fires(original_df, model):
    """
    Predict fire labels for live data using our traind model.
    Predictions are appended to dataframe in the 'fire' feature.
    """
    df = original_df.copy()
    
    df['fires'] = model.predict(df)
    
    return df

# def add_or_update_fires(df):
#     """
#     Adds predictions to our database.
#     """
#     df.to_sql('FireObservation', con=db, if_exists='append')

#     db.session.commit()


def check_new_df():
    """
    Pulls a new df from modis and compares it to the live df
    """
    new_df = pull_modis()

    #compares new_df to existing df, if equal it passes
    try:
        if assert_frame_equal(df, new_df):
            pass
        else:
            pass

    except:
        df = new_df.copy()
        return df        

#defines our first df from memory
# df = pd.read_csv('modus_df', sep=',')
df = pull_modis()
