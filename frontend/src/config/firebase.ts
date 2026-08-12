import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

/**
 * GuardianAI Google Firebase Authentication Configuration
 * Provides Real Google OAuth SSO via signInWithPopup.
 * Free Tier: 10,000 Phone SMS OTPs/month + Unlimited Email/Google Auth.
 */
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || 'AIzaSyABoh2-7rEpaAO0UH0yfdfJylt53AguEnA',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || 'guardianai-f6be8.firebaseapp.com',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || 'guardianai-f6be8',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || 'guardianai-f6be8.firebasestorage.app',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '915967269616',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || '1:915967269616:web:0adb775db3adcd6d1c8035',
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
