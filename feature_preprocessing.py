import math

import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler


def encode_with_LabelEncoder(df, column_name):
    label_encoder = LabelEncoder()
    label_encoder.fit(df[column_name])
    df[column_name+'_le'] = label_encoder.transform(df[column_name])
    df.drop([column_name], axis=1, inplace=True)
    return label_encoder


def encode_with_existing_LabelEncoder(df, column_name, label_encoder):
    df[column_name+'_le'] = label_encoder.transform(df[column_name])
    df.drop([column_name], axis=1, inplace=True)


def encode_with_OneHotEncoder_and_delete_column(df, column_name):
    le_encoder = encode_with_LabelEncoder(df, column_name)
    return perform_dummy_coding_and_delete_column(df, column_name, le_encoder), le_encoder


def encode_with_OneHotEncoder_using_existing_LabelEncoder_and_delete_column(df, column_name, le_encoder):
    encode_with_existing_LabelEncoder(df, column_name, le_encoder)
    return perform_dummy_coding_and_delete_column(df, column_name, le_encoder)


def perform_dummy_coding_and_delete_column(df, column_name, le_encoder):
    oh_encoder = OneHotEncoder(sparse=False)
    oh_features = oh_encoder.fit_transform(df[column_name+'_le'].values.reshape(-1,1))
    ohe_columns=[column_name + '=' + le_encoder.classes_[i] for i in range(oh_features.shape[1])]

    df.drop([column_name+'_le'], axis=1, inplace=True)
    
    df_with_features = pd.DataFrame(oh_features, columns=ohe_columns)
    df_with_features.index = df.index
    return pd.concat([df, df_with_features], axis=1)


def encode_with_func(df, column_name, func_name):
    df[column_name+'_le'] = df[column_name].map(func_name)
    df.drop(column_name, axis=1, inplace=True)


def month_to_decimal(month):
    month_dict = {'Jan':0, 'Feb':1/12., 'Mar':2/12., 'Apr':3/12., 'May':4/12., 'Jun':5/12., 
     'Jul':6/12., 'Aug':7/12., 'Sep':8/12., 'Oct':9/12., 'Nov':10/12., 'Dec':11/12.}
    return month_dict[month]


def convert_date(month_year):
    month_and_year = month_year.split('-')
    return float(month_and_year[1]) + month_to_decimal(month_and_year[0])


def processing_df(data_frame):
    data_frame['is_delinq_occurs'] = data_frame['mths_since_last_delinq'].map(lambda x: 0 if math.isnan(x) else 1)
    max_mths_since_last_delinq = np.nanmax(data_frame.mths_since_last_delinq.values)
    data_frame['mths_since_last_delinq'].fillna(max_mths_since_last_delinq, inplace=True)

    data_frame.fillna(0, inplace=True)
    data_frame.isnull().sum()

    grade_le_encoder = encode_with_LabelEncoder(data_frame,'grade')
    sub_grade_le_encoder = encode_with_LabelEncoder(data_frame,'sub_grade')

    encode_with_func(data_frame, 'issue_d', convert_date)
    encode_with_func(data_frame, 'earliest_cr_line', convert_date)

    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(data_frame)

    return scaled_df