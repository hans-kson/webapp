import flask
import pickle
import pandas as pd

# Use pickle to load in the pre-trained model
with open(f'model/loan_model_log_reg.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        LoanAmount = flask.request.form['LoanAmount']
        Combined_Income = flask.request.form['Combined_Income']
        

        # Make DataFrame for model
        input_variables = pd.DataFrame([[LoanAmount, Combined_Income]],
                                       columns=['LoanAmount', 'Combined_Income'],
                                       dtype=float,
                                       index=['input'])

        # Get the model's prediction
        #prediction = model.predict(input_variables)[0]
        def get_prediction(var_name):
            if var_name < 1:
                predict='Rejected'
            else:
                predict='Approved'
            return predict
    
        
        pred = model.predict(input_variables)[0]
        prediction = get_prediction(pred)
        
        
        
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('main.html',
                                     original_input={'LoanAmount':LoanAmount,
                                                     'Combined_Income':Combined_Income},                                                    
                                     result=prediction,
                                     )

if __name__ == '__main__':
    app.run()