import "firebase/database"
import { initializeApp } from 'firebase-admin';
import { collection, getDocs, getFirestore } from 'firebase/firestore';



var admin = require("firebase-admin");

var serviceAccount = require("path/to/serviceAccountKey.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

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
const example = collection(db, 'pass here'); // and example for passing a collection into firestore database
const docs = await getDocs(example); // get documentations