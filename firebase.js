import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

// Use config from window.firebaseConfig (loaded synchronously in index.html)
// or fallback to a placeholder if not loaded yet
const firebaseConfig = window.firebaseConfig || {
  apiKey: "MISSING_API_KEY",
  authDomain: "fair-ai.firebaseapp.com",
  projectId: "fair-ai",
  storageBucket: "fair-ai.firebasestorage.app",
  messagingSenderId: "892898039826",
  appId: "1:892898039826:web:429092ad366721350fe0cb"
};

if (firebaseConfig.apiKey === "MISSING_API_KEY") {
  console.warn("Firebase API Key is missing. Ensure the backend is running and providing the configuration.");
} else {
  console.log("Firebase initialized successfully with config from window.");
}

export const config = firebaseConfig;

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();
