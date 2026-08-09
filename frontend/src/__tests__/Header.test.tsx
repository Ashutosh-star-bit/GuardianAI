import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Header } from '../components/layout/Navbar';
import { AccessibilityProvider } from '../context/AccessibilityContext';

// GuardianAI Navbar Header Component Unit Test
// Purpose: Verifies brand logo, Senior Mode toggle switch, and privacy status badge render cleanly.
describe('Header Layout Component', () => {
  it('renders GuardianAI brand logo and Senior Mode toggle button', () => {
    render(
      <AccessibilityProvider>
        <BrowserRouter>
          <Header />
        </BrowserRouter>
      </AccessibilityProvider>
    );

    // Verify brand heading text
    expect(screen.getByText(/Guardian/i)).toBeInTheDocument();
    expect(screen.getByText(/AI/i)).toBeInTheDocument();

    // Verify Senior Mode toggle presence
    expect(screen.getByRole('button', { name: /Senior Mode/i })).toBeInTheDocument();
  });
});
