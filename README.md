# Ventilator Pressure Prediction

The task of this project is to predict ventilator air pressure supplied to patient's lung.

Correspondent dataset was taken from [Kaggle](https://www.kaggle.com/competitions/ventilator-pressure-prediction/overview).

## About the Data
The ventilator data was produced using a modified open-source ventilator connected to an artificial bellows test lung via a respiratory circuit. 

Ventilator has two control inputs. The first control input is a continuous variable from 0 to 100 representing the percentage the inspiratory solenoid valve is open to let air into the lung (i.e., 0 is completely closed and no air is let in and 100 is completely open). The second control input is a binary variable representing whether the exploratory valve is open (1) or closed (0) to let air out.

Dataset contains numerous time series of breaths. Each time series represents an approximately 3-second breath. 

### Dataset Columns
* id - globally-unique time step identifier across an entire file
* breath_id - globally-unique time step for breaths
* R - lung attribute indicating how restricted the airway is (in cmH2O/L/S). Physically, this is the change in pressure per change in flow (air volume per time). Intuitively, one can imagine blowing up a balloon through a straw. We can change R by changing the diameter of the straw, with higher R being harder to blow.
* C - lung attribute indicating how compliant the lung is (in mL/cmH2O). Physically, this is the change in volume per change in pressure. Intuitively, one can imagine the same balloon example. We can change C by changing the thickness of the balloon’s latex, with higher C having thinner latex and easier to blow.
time_step - the actual time stamp.
* u_in - the control input for the inspiratory solenoid valve. Ranges from 0 to 100.
* u_out - the control input for the exploratory solenoid valve. Either 0 or 1.
* pressure - the airway pressure measured in the respiratory circuit, measured in cmH2O.

## Data exploration

As was found pressure values varies very much for different `breath_id` as well as along `time_step` sequence.

The same even within unique sets of uniform parameters, i.e. for specific `R`, `C` and correspondent `time_step`.

With this specific problem data distribution it is hardly possible to judge which of the data are outliers and not the valid one. That is why dataset was considered as not applicable for outliers cleaning.

## Metrics

For metrics are choosen mean absolute error and mean absolute precentage error. Mean absolute error is not very much informative considering the problem, becouse it's difficult to evaluate how much error will influence breath process wereas mean absolute percentage error gives understanding about deviation from the true required value.




## Baseline

For baseline were taken LinearRegression and PolynomialRegression. Both of them demonstrated poor results and were substituted by RandomForestRegressor.

## Feature engineering

Along data exploration some additional features were added to the dataset. Primaly quite hamble dataset was expanded up to 28 features.

## Model

Final model - RandomForestRegressor produced result with average mean absoluter percentage error an about %4.5. 

Model's hyperparameters were defined by means `Optuna`.

# Conclusions

Best result was showed by RandomForestRegressor.

Model together with custom transformer were wrapped in pipeline prepared for model deploit. 

Docker image of the model with means of testing was created and placed on [Docker Hub](https://hub.docker.com/repository/docker/squir/web/general). 

To use server data in form of data frame with the same structure as original datase should be supplied by loading from file on a prompt. Send request to server by means `client.py`. Response - prediction from server will be received in the form of a list. 

Herewith attached test data frame `client_test_data_frame.csv` which can be used to test model.

Example of dataFrame for server request:

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>breath_id</th>
      <th>R</th>
      <th>C</th>
      <th>time_step</th>
      <th>u_in</th>
      <th>u_out</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>20</td>
      <td>50</td>
      <td>0.000000</td>
      <td>0.083334</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>20</td>
      <td>50</td>
      <td>0.033652</td>
      <td>18.383041</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1</td>
      <td>20</td>
      <td>50</td>
      <td>0.067514</td>
      <td>22.509278</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>