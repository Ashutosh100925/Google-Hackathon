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

export let auth = null;
export let provider = null;

try {
    const app = initializeApp(firebaseConfig);
    auth = getAuth(app);
    provider = new GoogleAuthProvider();
} catch (error) {
    console.error("Firebase initialization failed:", error);
}
