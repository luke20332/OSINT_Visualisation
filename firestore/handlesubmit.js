import { addDoc, collection } from "@firebase/firestore"
import { firestore } from "../firebase_setup/firebase"



var admin = require("firebase-admin");

var serviceAccount = require("path/to/serviceAccountKey.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});


const handlesubmit = (testdata) => { 
    const ref = collection(firestore, "test_data")

    let data = {
        testdata: testdata
    }
    try {
        addDoc(ref, data)
    } catch(err) {
        console.log(err)
    }
}

export default handlesubmit