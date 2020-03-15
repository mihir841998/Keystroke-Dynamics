from sklearn.externals import joblib
def authenticate_user(input_data):
    print('model input\n ',input_data)
    rfc=joblib.load('model.pkl')
    rfc_pred = rfc.predict(input_data)
    print(rfc_pred)
    return rfc_pred