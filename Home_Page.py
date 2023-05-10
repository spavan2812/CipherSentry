import streamlit as st 
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import re
import random
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import base64

from PIL import Image
from scipy.sparse import csr_matrix
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

st.set_page_config(page_title="CipherSentry",page_icon="toxic.jpg")

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT,password TEXT)')
def add_userdata(username,password):
    c.execute('INSERT INTO usertable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM usertable WHERE username =? AND password =?',(username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data


page_bg_color= """
<style> 
[data-testid="stheader"]{
background-color: #000101;
}

[data-testid="stSidebar"]{
background-color: #000101;
}

[data-testid="stAppViewContainer"] {
    background-color: #000000;
}

}
</style>
<h1 class = "head">Malicious URL and Fraudulent Credit Card Transaction detection system</h1>
"""

st.markdown(page_bg_color, unsafe_allow_html=True)

def getTokens(input):
    tokensBySlash = str(input.encode('utf-8')).split('/')
    allTokens = []
    for i in tokensBySlash:
        tokens = str(i).split('-')
        tokensByDot = []
        for j in range(0,len(tokens)):
            tempTokens = str(tokens[j]).split('.')
            tokensByDot = tokensByDot + tempTokens
            allTokens = allTokens + tokens + tokensByDot
            allTokens = list(set(allTokens))
            if 'com' in allTokens:
                allTokens.remove('com')
            return allTokens



def main():
    
    
    st.sidebar.success("Choose from the dropdown below")
    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Welcome to CipherSentry.")
        video_file = open('dangervideo.mp4', 'rb').read()
        video_bytes = base64.b64encode(video_file).decode('utf-8')
        st.markdown(f'<video autoplay loop width=480 height=270 src="data:video/mp4;base64,{video_bytes}"></video>', unsafe_allow_html=True)
        

    elif choice == "Login":
        st.subheader("Login Section")
        video_file = open('dangervideo.mp4', 'rb').read()
        video_bytes = base64.b64encode(video_file).decode('utf-8')
        st.markdown(f'<video autoplay loop width=480 height=270 src="data:video/mp4;base64,{video_bytes}"></video>', unsafe_allow_html=True)

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type= 'password')
        
        if st.sidebar.checkbox("Login"):
            #if password == '12345':
            create_usertable()
            result = login_user(username,password)
            if result:
                st.success("Logged in as {}".format(username))

                task = st.selectbox("Task",['Fraudulent Credit card transaction','Fraudulent URL detection system'])
                if task == "Fraudulent URL detection system":
                    st.subheader("Fraudulent URL detection system")
                    url = st.text_input('Enter a URL to check if it is malicious or not:')
                    submit_button = st.button('Check')
                    def trim(url):
                        return re.match(r'(?:\w*://)?(?:.*\.)?([a-zA-Z-1-9]*\.[a-zA-Z]{1,}).*', url).groups()[0]
                    
                    if submit_button:
                        model = joblib.load('mal-logireg1.pkl')
                        vectorizer = joblib.load("vectorizer1.pkl")
                        aa = csr_matrix(vectorizer.transform([trim(url)]))
                        s = model.predict(aa)
                        if s[0] == 0 :
                            
                            st.image('https://i.pinimg.com/originals/70/a5/52/70a552e8e955049c8587b2d7606cd6a6.gif', width=300)
                            st.success("This Website is Benign")
                        else:
                            
                            st.image('https://i.pinimg.com/originals/82/f9/df/82f9dfe3e1b4046f421735864c708d48.gif', width=300)
                            st.error("This website is Malicious")    


                elif task == "Fraudulent Credit card transaction":
                    data = pd.read_csv('creditcard.csv')
                    legit = data[data.Class == 0]
                    fraud = data[data.Class == 1]

                    legit_sample = legit.sample(n=len(fraud), random_state=2)
                    data = pd.concat([legit_sample, fraud], axis=0)
                    X = data.drop(columns="Class", axis=1)
                    y = data["Class"]
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=2)
                    model = LogisticRegression()
                    model.fit(X_train, y_train)
                    st.subheader("Fraud creditcard transaction")
                    input_df = st.text_input("Enter the fields")
                    input_df_lst = input_df.split(',')
                    submit = st.button("Submit")
                    if submit:
                        features = np.array(input_df_lst, dtype=np.float64)
                        prediction = model.predict(features.reshape(1, -1))
                        if prediction[0] == 0:
                            
                            st.image('https://i.pinimg.com/originals/70/a5/52/70a552e8e955049c8587b2d7606cd6a6.gif', width=300)
                            st.success("This was a Legitimate transaction")
                        else:
                            
                            st.image('https://i.pinimg.com/originals/82/f9/df/82f9dfe3e1b4046f421735864c708d48.gif', width=300) 
                            st.error("This was a Fraudulent transaction")
            else:
                st.warning("Incorrect Password")        
    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,new_password)
            st.success("You have successfully created an valid Account")
            st.info("Go to Login Menu to login")



    
if __name__ == '__main__':
    main()


