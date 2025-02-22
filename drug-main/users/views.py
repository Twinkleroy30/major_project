# # rewriting code with password hashing
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.files.storage import FileSystemStorage
# from django.contrib.auth.hashers import make_password
# from .models import User

# def register(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         mobile = request.POST.get('mobile')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         age = request.POST.get('age')
#         address = request.POST.get('address')

#         profile_picture = request.FILES.get('profile_picture')  # Handle file upload

#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email already registered')
#             return redirect('userregister')

#         hashed_password = make_password(password)
#         user = User(name=name, mobile=mobile, email=email, password=hashed_password, age=age, address=address)

#         if profile_picture:
#             try:
#                 fs = FileSystemStorage()
#                 filename = fs.save(profile_picture.name, profile_picture)
#                 user.profile_picture = filename
#             except Exception as e:
#                 messages.error(request, 'Profile picture upload failed: ' + str(e))
#                 return redirect('userregister')

#         user.save()

#         messages.success(request, 'Registration successful! Please login.')
#         return redirect('userlogin')

#     return render(request, 'user/register.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from .models import User

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        age = request.POST.get('age')
        address = request.POST.get('address')

        profile_picture = request.FILES.get('profile_picture')  # Handle file upload

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('userregister')

        hashed_password = make_password(password)
        user = User(name=name, mobile=mobile, email=email, password=hashed_password, age=age, address=address)

        if profile_picture:
            try:
                fs = FileSystemStorage()
                if not profile_picture.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    messages.error(request, 'Invalid file type. Please upload a .png, .jpg, or .jpeg file.')
                    return redirect('userregister')
                if profile_picture.size > 5 * 1024 * 1024:  # 5 MB limit
                    messages.error(request, 'File too large. Please upload a file smaller than 5 MB.')
                    return redirect('userregister')
                filename = fs.save(profile_picture.name, profile_picture)
                user.profile_picture = fs.url(filename)
            except Exception as e:
                messages.error(request, 'Profile picture upload failed: ' + str(e))
                print(str(e))
                return redirect('userregister')

        user.save()

        messages.success(request, 'Registration successful! Please login.')
        return redirect('userlogin')

    return render(request, 'user/register.html')


# def userlogin(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')  # Get the username or email
#         password = request.POST.get('password')  # Get the password

#         # Check if the user exists and the password is correct
#         try:
#             user = User.objects.get(email=email)
#             if user.password == password:  # Be cautious about plain text password comparison
#                 # Log the user in (you may want to set a session or token here)
#                 request.session['user_id'] = user.id  # Store user ID in session
#                 messages.success(request, 'Login successful!')
#                 return redirect('udashboard')  # Redirect to the index page or desired page
#             else:
#                 messages.error(request, 'Invalid email or password. Please try again.')
#         except User.DoesNotExist:
#             messages.error(request, 'Invalid email or password. Please try again.')

#     return render(request, 'user/userlogin.html')

# rewriting code with password hashing
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import User

def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):  # Secure password check
                request.session['user_id'] = user.id  # Store user ID in session
                messages.success(request, 'Login successful!')
                return redirect('udashboard')  # Redirect to the desired page
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'user/userlogin.html')




def udashboard(req):
    return render (req, 'user/udashboard.html')

# import pickle
# import pandas as pd
# from django.shortcuts import render
# from django.http import JsonResponse

# # Load the trained model from the pickle file
# with open('cnn_model.pkl', 'rb') as f:
#     model = pickle.load(f)  # Load the model only

# def prediction(request):
#     if request.method == 'POST':
#         # Get data from POST request
#         patient_id = request.POST.get('patient_id')
#         age = request.POST.get('age')
#         gender = request.POST.get('gender')
#         disease_type = request.POST.get('disease_type')
#         drug_name = request.POST.get('drug_name')
#         dosage = request.POST.get('dosage')
#         treatment_duration = request.POST.get('treatment_duration')
#         drug_efficacy = request.POST.get('drug_efficacy')

#         # Validate input data
#         if not all([patient_id, age, gender, disease_type, drug_name, dosage, treatment_duration, drug_efficacy]):
#             return JsonResponse({'error': 'All fields are required.'}, status=400)

#         # Convert inputs to appropriate types
#         age = float(age)
#         dosage = float(dosage)
#         treatment_duration = float(treatment_duration)
#         drug_efficacy = float(drug_efficacy)

#         # Prepare input data
#         input_data = {
#             'Patient ID': [patient_id],
#             'Age': [age],
#             'Gender': [gender],
#             'Disease Type': [disease_type],
#             'Drug Name': [drug_name],
#             'Dosage (mg)': [dosage],
#             'Treatment Duration (days)': [treatment_duration],
#             'Drug Efficacy (%)': [drug_efficacy]
#         }

#         input_df = pd.DataFrame(input_data)

#         # Convert categorical variables to numerical
#         input_df['Gender'] = input_df['Gender'].map({'Male': 0, 'Female': 1})  # Encoding for gender
#         input_df['Disease Type'] = input_df['Disease Type'].astype('category').cat.codes  # Encoding for disease type
#         input_df['Drug Name'] = input_df['Drug Name'].astype('category').cat.codes  # Encoding for drug name

#         # Ensure the right input shape for your model
#         # Check the expected input shape of the model
#         expected_shape = model.input_shape  # This will help you determine how to reshape
        
#         # Prepare input to match model input requirements
#         if expected_shape[1] == input_df.shape[1]:  # If number of features matches
#             X_processed = input_df.values.astype('float32').reshape(1, input_df.shape[1])  # Shape (1, 8)
#         else:
#             # If shape doesn't match, handle accordingly (e.g., adding dummy features)
#             while input_df.shape[1] < expected_shape[1]:
#                 input_df['Dummy Feature ' + str(input_df.shape[1])] = 0.0  # Add dummy features
#             X_processed = input_df.values.astype('float32').reshape(1, input_df.shape[1])  # Adjust the shape

#         # Make predictions
#         prediction = (model.predict(X_processed) > 0.5).astype("int32")[0][0]

#         # Map the prediction to response
#         response = 'Drug Efficiency' if prediction == 1 else 'Drug is not Efficiency'

#         return JsonResponse({'prediction': response})

#     # Render the prediction form for GET requests
#     return render(request, 'user/prediction.html')




import joblib
import numpy as np
import tensorflow as tf

from sklearn.preprocessing import LabelEncoder
from django.shortcuts import render
import pandas as pd


# Load model, scaler, and feature names
model = tf.keras.models.load_model("cnn_drug_discovery_model.h5")
scaler = joblib.load("scalers.pkl")
expected_features = joblib.load("feature_names.pkl")  # Load expected feature names
print("Model, scaler, and feature names loaded successfully!")

# Define label encoders
label_encoders = {
    "Gender": LabelEncoder().fit(["Male", "Female"]),
    "Medical_History": LabelEncoder().fit(["Diabetes", "Hypertension", "Cancer", "None"]),
    "Drug_Name": LabelEncoder().fit(["DrugA", "DrugB", "DrugC", "DrugD"]),
    "Side_Effects": LabelEncoder().fit(["None", "Nausea", "Dizziness", "Fatigue"]),
    "Disease_Type": LabelEncoder().fit(["Lung Cancer", "Breast Cancer", "Diabetes", "Heart Disease"]),
    "Genetic_Marker": LabelEncoder().fit(["MarkerA", "MarkerB", "MarkerC", "MarkerD"])
}

# Django view for both rendering the form and processing predictions
def prediction(request):
    prediction_text = None
    medications = []

    if request.method == 'POST':
        input_data = {}

        for feature in expected_features:
            value = request.POST.get(feature)
            if feature in label_encoders and value is not None:
                value = label_encoders[feature].transform([value])[0]
            else:
                value = float(value) if value is not None else 0
            input_data[feature] = value
        
        # Convert input data to NumPy array in correct order
        input_array = np.array([input_data[feature] for feature in expected_features]).reshape(1, -1)

        # Normalize input using the pre-trained scaler
        input_array = scaler.transform(input_array)

        # Reshape for CNN input
        input_array = np.expand_dims(input_array, axis=2)

        # Make prediction
        prediction = model.predict(input_array)
        effectiveness_score = prediction[0][0] * 100  # Convert to percentage
        prediction_text = f'Predicted Drug Effectiveness: {effectiveness_score:.2f}%'
        
        # Get disease type from input data
        disease_type = request.POST.get('Disease_Type')
        print(f"Disease Type: {disease_type}")
        if disease_type:
            # Load medications data
            med_df = pd.read_csv('medications.csv')
            print(f"Loaded Medications CSV: {med_df.head()}")
            # Find medications for the predicted disease
            matched_medications = med_df[med_df['Disease'] == disease_type]
            print(f"Matched Medications: {matched_medications}")  
            
            # Get medications for the predicted disease                       
            if not matched_medications.empty:
                medications = matched_medications['Medication'].tolist()  # Convert to list
            else:
                messages.warning(request, 'No medication information found for this condition.')

    return render(request, 'user/prediction.html', {
        'prediction_text': prediction_text,
        'medications': medications
    })



def medication(req):
    medications = req.GET.get('medications', '')
    # Convert string representation of list to actual list
    if medications.startswith('[') and medications.endswith(']'):
        medications = eval(medications)
    return render(req, 'user/medication.html', {'medications': medications})

# predict module methods


from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
import pandas as pd
import pickle



# Load datasets
sym_des = pd.read_csv(r"symtoms_df.csv")
precautions = pd.read_csv(r"precautions_df.csv")
workout = pd.read_csv(r"workout_df.csv")
description = pd.read_csv(r"description.csv")
medications = pd.read_csv(r"medications.csv")
diets = pd.read_csv(r"diets.csv")

# Load model
svc = pickle.load(open(r"svc.pkl", 'rb'))

# Helper function
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis]['workout']

    return desc, pre, med, die, wrkout

symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

# Model Prediction function
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]

# Index view
def index(request):
    return render(request, 'user/medication.html')

# Predict view
def predict(request):
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')
        if symptoms == "Symptoms" or symptoms == "":
            messages.warning(request, 'Please either write symptoms or you have written misspelled symptoms')
            #return render(request, 'user/medication.html', {'message': message})
        else:
            user_symptoms = [s.strip() for s in symptoms.split(',')]
            user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
            print(f'User symptoms: {user_symptoms}')
            predicted_disease = get_predicted_value(user_symptoms)
            dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

            my_precautions = [i for i in precautions[0]]

            options = ['select_symptom', 'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']

            if not medications:
                medications = []
                messages.warning(request, 'No medication information found for this condition.')
            else:
                medications = medications[0].split(', ')
               
            
            if not rec_diet:
                rec_diet = []
                messages.warning(request, 'No Diet information found for this condition.')
            else:
                rec_diet = rec_diet[0].split(', ')
                
                print(dis_des)
                print(precautions)
                print(medications)
                print(rec_diet)
                print(workout)

            return render(request, 'user/medication.html', {
                'predicted_disease': predicted_disease,
                'dis_des': dis_des,
                'my_precautions': my_precautions,
                'medications': medications,
                'my_diet': rec_diet,
                'workout': workout,
                'options': options,
                'user_symptoms': user_symptoms
            })
        
    return render(request, 'user/medication.html')
