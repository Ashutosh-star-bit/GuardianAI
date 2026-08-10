import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, GithubAuthProvider } from 'firebase/auth';

/**
 * GuardianAI Google Firebase Authentication Configuration
 * Provides 10,000 Free Phone SMS OTPs / month, 1-Click Google/GitHub SSO, and Email Auth.
 */
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || 'AIzaSyABoh2-7rEpaA00UH0yfdfJylt53AguEnA',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || 'guardianai-f6be8.firebaseapp.com',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || 'guardianai-f6be8',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || 'guardianai-f6be8.firebasestorage.app',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '915967269616',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || '1:915967269616:web:0adb775db3adcd6d1c8035',
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
export const githubProvider = new GithubAuthProvider();
