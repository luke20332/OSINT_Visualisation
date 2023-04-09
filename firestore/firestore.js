const { initializeApp, applicationDefault, cert } = require('firebase-admin/app');
const { getFirestore, Timestamp, FieldValue } = require('firebase-admin/firestore');

const serviceAccount = require('C:\Users\Glonk\OneDrive\Documents\GitHub\OSINT_Visualisation\firestore'); //local path

initializeApp({
  credential: cert(serviceAccount)
});

const db = getFirestore();