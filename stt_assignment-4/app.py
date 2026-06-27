import streamlit as st
import pickle
import pandas as pd

#Loading the model
with open("models/best_rf_model.pkl","rb") as f:
    model=pickle.load(f)
with open("models/encoders.pkl","rb") as f:
    encoders=pickle.load(f)
st.title("URBAN NEST ANALYTICS - THE RENT PREDICTOR")
city=st.selectbox("City",encoders["city"].classes_)
location=st.selectbox("Location",encoders["location"].classes_)
latitude=st.number_input("Latitude",value=19.01)
if latitude < 18.15 or latitude > 30.89:
    st.warning(" Latitude is outside the trained cities range (18.15 - 30.89). Prediction may be inaccurate.")
longitude=st.number_input("Longitude",value=74.6)
if longitude < 72.8 or longitude > 90.4:
    st.warning(" Longitude is outside the trained cities range (72.8 - 90.4). Prediction may be inaccurate.")
bathroom=st.slider("No.of Bathrooms",0,10,value=1)
balconies=st.slider("No.of Balconies",0,8,value=1)
negotiable=st.selectbox("is_Negotiable- 0 for No, 1 for Yes",[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
security_deposit=st.number_input("Security Deposit in INR",value=50000.1)
status=st.selectbox("Status",encoders["Status"].classes_)
size=st.number_input("Size in sqft",value=1709.4)
bhk=st.slider("BHK",0,1,value=1)
rooms_num=st.slider("Number of Rooms",1,10,value=2)
property_type=st.selectbox("Property Type",encoders["property_type"].classes_)
verification_days=st.number_input("Verification Days",value=343.0)
#st.write(model.feature_names_in_.tolist())
if st.button("Predict"):
    #encoding categorical features into numeric for analysis
    
    city_encoded=encoders["city"].transform([city])[0]
    location_encoded=encoders["location"].transform([location])[0]
    status_encoded=encoders["Status"].transform([status])[0]
    property_type_encoded=encoders["property_type"].transform([property_type])[0]
    df=pd.DataFrame([{
        "location":location_encoded,
        "city":city_encoded,        
        "latitude":latitude,
        "longitude":longitude,
        "numBathrooms":bathroom,
        "numBalconies":balconies,
        "isNegotiable":negotiable,
        "SecurityDeposit":security_deposit,
        "Status":status_encoded,
        "Size_ft²":size,
        "BHK":bhk,
        "rooms_num":rooms_num,
        "property_type":property_type_encoded,
        "verification_days":verification_days
    }])
    prediction=model.predict(df)[0]
    st.success(f"The predicted rent price is: {prediction: .4f} INR")
# Build your Streamlit application here
