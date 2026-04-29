import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

// Use config from window.firebaseConfig (loaded from /api/firebase-config-js)
// or fallback to a placeholder if not loaded yet
const firebaseConfig = window.firebaseConfig || {
  apiKey: "MISSING_API_KEY",
  authDomain: "fair-ai.firebaseapp.com",
  projectId: "fair-ai",
  storageBucket: "fair-ai.firebasestorage.app",
  messagingSenderId: "892898039826",
  appId: "1:892898039826:web:429092ad366721350fe0cb"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();
