import React from 'react';
import { initializeApp } from 'firebase-admin';
import ReactDOM from 'react-dom/client';
//import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { collection, getDocs, getFirestore } from 'firebase/firestore';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  
    <App />
  
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

const firebaseConfig = {
    apiKey: "AIzaSyCF1woH6v_CVi9J_5lCfcdQRT9CeDFTmQo",
    authDomain: "osint-ads-23.firebaseapp.com",
    databaseURL: "https://osint-ads-23-default-rtdb.firebaseio.com",
    projectId: "osint-ads-23",
    storageBucket: "osint-ads-23.appspot.com",
    messagingSenderId: "813958012003",
    appId: "1:813958012003:web:f8b2277e401e224e0b6c56",
    measurementId: "G-6E5TST6JM3"
  };

const  firebaseApp = initializeApp(firebaseConfig);
const db = getFirestore(firebaseApp);
/*const example = collection(db, 'pass here'); // and example for passing a collection into firestore database
const docs = await getDocs(example); // get documentations*/


