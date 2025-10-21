/**
 * Settings API Service
 * Handles all communication with the backend settings API
 */

const API_BASE_URL = 'http://localhost:8000/api/settings';

export interface ProfileSettings {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  timezone: string;
  language: string;
  date_format: string;
  currency: string;
}

export interface NotificationSetting {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  type: 'email' | 'push' | 'sms';
}

export interface TradingPreferences {
  default_order_type: string;
  default_quantity: number;
  confirm_before_order: boolean;
  show_advanced_options: boolean;
  auto_square_off: boolean;
  risk_warnings: boolean;
  max_position_size: number;
  stop_loss_default: number;
}

export interface AppearanceSettings {
  theme: 'dark' | 'light' | 'auto';
  chart_positive_color: string;
  chart_negative_color: string;
}

export interface UserSettings {
  profile: ProfileSettings;
  notifications: NotificationSetting[];
  trading: TradingPreferences;
  appearance: AppearanceSettings;
}

export interface APIKeyData {
  provider: string;
  api_key: string;
  api_secret?: string;
  app_id?: string;
  redirect_url?: string;
  extra_fields?: Record<string, any>;
}

export interface APIKeyResponse {
  provider: string;
  api_key_masked: string;
  created_at: string;
  updated_at: string;
}

/**
 * Fetch all user settings
 */
export async function getAllSettings(): Promise<UserSettings> {
  const response = await fetch(`${API_BASE_URL}/`);
  if (!response.ok) {
    throw new Error('Failed to fetch settings');
  }
  return response.json();
}

/**
 * Update all user settings
 */
export async function updateAllSettings(settings: UserSettings): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(settings),
  });
  if (!response.ok) {
    throw new Error('Failed to update settings');
  }
  return response.json();
}

/**
 * Get profile settings
 */
export async function getProfile(): Promise<ProfileSettings> {
  const response = await fetch(`${API_BASE_URL}/profile`);
  if (!response.ok) {
    throw new Error('Failed to fetch profile');
  }
  return response.json();
}

/**
 * Update profile settings
 */
export async function updateProfile(profile: ProfileSettings): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/profile`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(profile),
  });
  if (!response.ok) {
    throw new Error('Failed to update profile');
  }
  return response.json();
}

/**
 * List all API keys (masked)
 */
export async function listAPIKeys(): Promise<APIKeyResponse[]> {
  const response = await fetch(`${API_BASE_URL}/api-keys`);
  if (!response.ok) {
    throw new Error('Failed to fetch API keys');
  }
  return response.json();
}

/**
 * Add or update an API key
 */
export async function saveAPIKey(keyData: APIKeyData): Promise<{ message: string; masked_key: string }> {
  const response = await fetch(`${API_BASE_URL}/api-keys`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(keyData),
  });
  if (!response.ok) {
    throw new Error('Failed to save API key');
  }
  return response.json();
}

/**
 * Get decrypted API key for a specific provider
 */
export async function getAPIKey(provider: string): Promise<APIKeyData> {
  const response = await fetch(`${API_BASE_URL}/api-keys/${provider}`);
  if (!response.ok) {
    throw new Error('Failed to fetch API key');
  }
  return response.json();
}

/**
 * Delete an API key
 */
export async function deleteAPIKey(provider: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/api-keys/${provider}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to delete API key');
  }
  return response.json();
}

/**
 * Health check for settings API
 */
export async function healthCheck(): Promise<{ status: string; message: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error('Health check failed');
  }
  return response.json();
}

/**
 * Convert frontend profile data to API format
 */
export function convertProfileToAPI(frontendProfile: any): ProfileSettings {
  return {
    first_name: frontendProfile.firstName,
    last_name: frontendProfile.lastName,
    email: frontendProfile.email,
    phone: frontendProfile.phone,
    timezone: frontendProfile.timezone,
    language: frontendProfile.language,
    date_format: frontendProfile.dateFormat,
    currency: frontendProfile.currency,
  };
}

/**
 * Convert API profile data to frontend format
 */
export function convertProfileFromAPI(apiProfile: ProfileSettings): any {
  return {
    firstName: apiProfile.first_name,
    lastName: apiProfile.last_name,
    email: apiProfile.email,
    phone: apiProfile.phone,
    timezone: apiProfile.timezone,
    language: apiProfile.language,
    dateFormat: apiProfile.date_format,
    currency: apiProfile.currency,
  };
}

/**
 * Convert frontend trading preferences to API format
 */
export function convertTradingToAPI(frontendTrading: any): TradingPreferences {
  return {
    default_order_type: frontendTrading.defaultOrderType,
    default_quantity: frontendTrading.defaultQuantity,
    confirm_before_order: frontendTrading.confirmBeforeOrder,
    show_advanced_options: frontendTrading.showAdvancedOptions,
    auto_square_off: frontendTrading.autoSquareOff,
    risk_warnings: frontendTrading.riskWarnings,
    max_position_size: frontendTrading.maxPositionSize,
    stop_loss_default: frontendTrading.stopLossDefault,
  };
}

/**
 * Convert API trading preferences to frontend format
 */
export function convertTradingFromAPI(apiTrading: TradingPreferences): any {
  return {
    defaultOrderType: apiTrading.default_order_type,
    defaultQuantity: apiTrading.default_quantity,
    confirmBeforeOrder: apiTrading.confirm_before_order,
    showAdvancedOptions: apiTrading.show_advanced_options,
    autoSquareOff: apiTrading.auto_square_off,
    riskWarnings: apiTrading.risk_warnings,
    maxPositionSize: apiTrading.max_position_size,
    stopLossDefault: apiTrading.stop_loss_default,
  };
}
