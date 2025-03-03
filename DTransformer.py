from sklearn.base import TransformerMixin, BaseEstimator
import pandas as pd

# declare custom transformer
class DTransformer(TransformerMixin, BaseEstimator):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        
        time_step_max = X.groupby('breath_id').time_step.idxmax()
        # u_in correspondent to time_step_max
        last_u_in = X.loc[time_step_max, ['breath_id','u_in']]
        # add feature last_u_in
        last_u_in.rename(columns={'u_in':'last_u_in'}, inplace=True)
        X = X.merge(last_u_in, on='breath_id')
        # add feature mean u_in
        mean_u_in = X.groupby('breath_id')['u_in'].mean().to_frame()
        mean_u_in.rename(columns={'u_in':'mean_u_in'}, inplace=True)
        X = X.merge(mean_u_in, on='breath_id')
        X['diff_u_in'] = X.groupby('breath_id')['u_in'].diff()
        X = X.fillna(0)
        X['diff2_u_in'] = X.groupby('breath_id')['diff_u_in'].diff()
        X = X.fillna(0)
        X['u_in_cumsum'] = (X['u_in']).groupby(X['breath_id']).cumsum()
        # add feature sum value u_in
        sum_u_in = X.groupby('breath_id')['u_in'].sum().to_frame()
        sum_u_in.columns = ['sum_value_u_in']
        X = X.merge(sum_u_in,on='breath_id')
        # add feature u_in_cumsum_rate
        X["u_in_cumsum_rate"] = X["u_in_cumsum"] / X["sum_value_u_in"]
        X = X.fillna(0)
        # add feature: lag of u_in
        X['lag_u_in'] = X.groupby('breath_id')['u_in'].shift(1)
        X = X.fillna(0)

        # add feature: lag2 of u_in
        X['lag_2_u_in'] = X.groupby('breath_id')['u_in'].shift(2)
        X = X.fillna(0)
        # add feature lag -1 and -2 u_in
        X['lag_-1_u_in'] = X.groupby('breath_id')['u_in'].shift(-1)
        X = X.fillna(0)

        X['lag_-2_u_in'] = X.groupby('breath_id')['u_in'].shift(-2)
        X = X.fillna(0)
        # add feature lag -3 and 3 u_in
        X['lag_-3_u_in'] = X.groupby('breath_id')['u_in'].shift(-3)
        X = X.fillna(0)

        X['lag_3_u_in'] = X.groupby('breath_id')['u_in'].shift(3)
        X = X.fillna(0)
        # add feature max_u_in_breathid
        X["max_u_in_breathid"] = X.groupby("breath_id")["u_in"].transform("max")

        # add feature R*C
        X["R*C"] = X['R'] * X['C']

        # add breath_id__u_in__min
        X['breath_id__u_in__min'] = X.groupby(['breath_id'])['u_in'].transform('min')

        # add breath_id__u_in__diffmax and breath_id__u_in__diffmean
        X['breath_id__u_in__diffmax'] = X.groupby(['breath_id'])['u_in'].transform('max') - X['u_in']
        X['breath_id__u_in__diffmean'] = X.groupby(['breath_id'])['u_in'].transform('mean') - X['u_in']

        X['u_in_partition_out_sum'] = X.groupby(['breath_id',"u_out"])['u_in'].transform("sum")

        # add feature area
        X['area'] = X['time_step'] * X['u_in']
        X['area'] = X.groupby('breath_id')['area'].cumsum()
        ##add feature time_diff
        X['time_diff']=X.time_step.diff().fillna(0)
        X.drop('breath_id', axis=1, inplace=True)
        
        return X