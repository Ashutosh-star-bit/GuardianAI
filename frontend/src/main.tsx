import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';

// GuardianAI React Application Main Entrypoint
// Purpose: Mounts root App component into HTML DOM with React Strict Mode enabled.
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
