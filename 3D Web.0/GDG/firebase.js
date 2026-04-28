import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyBlF9F4XmeQnnpj8wcsrqkmnKYvlNkS2wE",
  authDomain: "fair-ai.firebaseapp.com",
  projectId: "fair-ai",
  storageBucket: "fair-ai.firebasestorage.app",
  messagingSenderId: "892898039826",
  appId: "1:892898039826:web:429092ad366721350fe0cb"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();
