import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyAxFq7ZxdUzXmMFpch2PY4rzphz9igqJuo",
  authDomain: "kojiawarness-test.firebaseapp.com",
  projectId: "kojiawarness-test",
  storageBucket: "kojiawarness-test.appspot.com",
  messagingSenderId: "144394442464",
  appId: "1:144394442464:web:5700592104fbe38af4a285",
  measurementId: "G-YSDWM7LX24"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export { app, analytics };