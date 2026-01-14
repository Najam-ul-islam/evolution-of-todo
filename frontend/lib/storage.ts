// lib/storage.ts
export const setItem = (key: string, value: any): void => {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.error(`Error setting item ${key}:`, error);
  }
};

export const getItem = (key: string): any => {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
  } catch (error) {
    console.error(`Error getting item ${key}:`, error);
    return null;
  }
};

export const removeItem = (key: string): void => {
  try {
    localStorage.removeItem(key);
  } catch (error) {
    console.error(`Error removing item ${key}:`, error);
  }
};

export const clearStorage = (): void => {
  try {
    localStorage.clear();
  } catch (error) {
    console.error('Error clearing storage:', error);
  }
};

// Session-specific utilities
export const setSession = (session: any): void => {
  setItem('session', session);
};

export const getSession = (): any => {
  return getItem('session');
};

export const removeSession = (): void => {
  removeItem('session');
};

export const setCurrentUser = (user: any): void => {
  setItem('user', user);
};

export const getCurrentUser = (): any => {
  return getItem('user');
};

export const removeCurrentUser = (): void => {
  removeItem('user');
};