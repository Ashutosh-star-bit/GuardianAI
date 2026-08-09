import { z } from 'zod';

/**
 * GuardianAI Zod Validation Schemas
 * Purpose: Provides type-safe validation schemas for scan inputs, user authentication, and profile forms.
 */

export const textScanSchema = z.object({
  payload: z
    .string()
    .min(3, 'Message must be at least 3 characters long')
    .max(5000, 'Message cannot exceed 5000 characters'),
  zeroKnowledge: z.boolean().default(false),
});

export const urlScanSchema = z.object({
  url: z.string().url('Please enter a valid URL (e.g. https://example.com)'),
});

export const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters long'),
});

export type TextScanFormData = z.infer<typeof textScanSchema>;
export type UrlScanFormData = z.infer<typeof urlScanSchema>;
export type LoginFormData = z.infer<typeof loginSchema>;
