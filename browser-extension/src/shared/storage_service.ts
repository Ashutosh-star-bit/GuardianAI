/**
 * GuardianAI Extension Storage Service Subsystem
 * Purpose: Centralized, quota-aware storage manager encapsulating chrome.storage.local and chrome.storage.sync:
 *          - Manages Recent Scans History (max 20 entries)
 *          - Manages Settings & User Preferences in chrome.storage.sync
 *          - Manages Cached Analysis LRU entries with automatic TTL eviction & 2,000 item capacity caps
 *          - Storage Quota Monitoring (chrome.storage.local 10MB limit, sync 100KB limit).
 */

import { ExtensionScanResult, ExtensionSettings } from './types';

export interface StorageQuotaInfo {
  local_bytes_used: number;
  local_quota_bytes: number;
  local_usage_pct: number;
  sync_bytes_used: number;
  sync_quota_bytes: number;
  sync_usage_pct: number;
}

export class ExtensionStorageService {
  private static CACHE_PREFIX = 'cache_url_';
  private static RECENT_SCANS_KEY = 'recent_scans';
  private static SETTINGS_KEY = 'settings';
  private static MAX_RECENT_SCANS = 20;
  private static MAX_CACHE_ENTRIES = 2000;
  private static CACHE_TTL_MS = 3600 * 1000; // 1 hour

  // --- 1. USER SETTINGS & PREFERENCES (SYNC STORAGE WITH LOCAL FALLBACK) ---

  public static async getSettings(): Promise<ExtensionSettings> {
    try {
      const syncData = await chrome.storage.sync.get(this.SETTINGS_KEY);
      if (syncData[this.SETTINGS_KEY]) {
        return syncData[this.SETTINGS_KEY];
      }
    } catch {
      // Storage sync fallback
    }

    const localData = await chrome.storage.local.get(this.SETTINGS_KEY);
    return localData[this.SETTINGS_KEY] || this.getDefaultSettings();
  }

  public static async saveSettings(settings: Partial<ExtensionSettings>): Promise<ExtensionSettings> {
    const current = await this.getSettings();
    const updated = { ...current, ...settings };

    try {
      await chrome.storage.sync.set({ [this.SETTINGS_KEY]: updated });
    } catch {
      await chrome.storage.local.set({ [this.SETTINGS_KEY]: updated });
    }

    return updated;
  }

  // --- 2. RECENT SCANS HISTORY MANAGEMENT ---

  public static async getRecentScans(): Promise<ExtensionScanResult[]> {
    const data = await chrome.storage.local.get(this.RECENT_SCANS_KEY);
    return data[this.RECENT_SCANS_KEY] || [];
  }

  public static async addRecentScan(result: ExtensionScanResult): Promise<ExtensionScanResult[]> {
    const existing = await this.getRecentScans();
    // Filter out duplicates of same domain
    const filtered = existing.filter((r) => r.domain !== result.domain);
    const updated = [result, ...filtered].slice(0, this.MAX_RECENT_SCANS);

    await chrome.storage.local.set({ [this.RECENT_SCANS_KEY]: updated });
    return updated;
  }

  public static async clearRecentScans(): Promise<void> {
    await chrome.storage.local.remove(this.RECENT_SCANS_KEY);
  }

  // --- 3. DOMAIN THREAT LRU CACHING ---

  public static async getCachedAnalysis(domain: string): Promise<ExtensionScanResult | null> {
    const cacheKey = `${this.CACHE_PREFIX}${domain}`;
    const data = await chrome.storage.local.get(cacheKey);

    if (data[cacheKey]) {
      const entry: { result: ExtensionScanResult; timestamp: number } = data[cacheKey];
      if (Date.now() - entry.timestamp < this.CACHE_TTL_MS) {
        return entry.result;
      }
      // Expired entry
      await chrome.storage.local.remove(cacheKey);
    }
    return null;
  }

  public static async setCachedAnalysis(domain: string, result: ExtensionScanResult): Promise<void> {
    const cacheKey = `${this.CACHE_PREFIX}${domain}`;
    await this.ensureCacheCapacity();

    await chrome.storage.local.set({
      [cacheKey]: { result, timestamp: Date.now() }
    });
  }

  public static async clearAllCache(): Promise<void> {
    const all = await chrome.storage.local.get(null);
    const cacheKeys = Object.keys(all).filter((k) => k.startsWith(this.CACHE_PREFIX));
    if (cacheKeys.length > 0) {
      await chrome.storage.local.remove(cacheKeys);
    }
  }

  // --- 4. STORAGE QUOTA & CAPACITY MONITORING ---

  public static async getStorageQuotaInfo(): Promise<StorageQuotaInfo> {
    const localBytes = await chrome.storage.local.getBytesInUse(null);
    const localQuota = chrome.storage.local.QUOTA_BYTES || 10485760; // 10MB default
    const syncBytes = await chrome.storage.sync.getBytesInUse(null);
    const syncQuota = chrome.storage.sync.QUOTA_BYTES || 102400; // 100KB default

    return {
      local_bytes_used: localBytes,
      local_quota_bytes: localQuota,
      local_usage_pct: Math.round((localBytes / localQuota) * 10000) / 100,
      sync_bytes_used: syncBytes,
      sync_quota_bytes: syncQuota,
      sync_usage_pct: Math.round((syncBytes / syncQuota) * 10000) / 100
    };
  }

  private static async ensureCacheCapacity(): Promise<void> {
    const all = await chrome.storage.local.get(null);
    const cacheKeys = Object.keys(all).filter((k) => k.startsWith(this.CACHE_PREFIX));

    if (cacheKeys.length >= this.MAX_CACHE_ENTRIES) {
      // Sort entries by timestamp (oldest first)
      const sorted = cacheKeys.map((k) => ({
        key: k,
        timestamp: all[k]?.timestamp || 0
      })).sort((a, b) => a.timestamp - b.timestamp);

      // Evict oldest 200 entries (LRU pruning)
      const keysToEvict = sorted.slice(0, 200).map((item) => item.key);
      await chrome.storage.local.remove(keysToEvict);
      console.log(`[GuardianAI StorageService] LRU Pruning evicted ${keysToEvict.length} oldest cache items.`);
    }
  }

  private static getDefaultSettings(): ExtensionSettings {
    return {
      senior_mode: true,
      auto_block_critical: true,
      sound_alerts: true,
      highlight_links: true,
      api_endpoint: 'http://localhost:8000/api/v1'
    };
  }
}
