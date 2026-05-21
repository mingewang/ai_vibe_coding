import { createContext, useContext, useState, useMemo, ReactNode } from 'react';
import { useColorScheme } from 'react-native';

type Theme = {
  background: string;
  surface: string;
  primary: string;
  primaryLight: string;
  text: string;
  textSecondary: string;
  accent: string;
  border: string;
  tabBar: string;
  tabBarBorder: string;
  cardShadow: string;
  inputBackground: string;
  statusBar: 'dark' | 'light';
  headerTint: string;
};

type ThemeContextType = {
  isDark: boolean;
  theme: Theme;
  toggleTheme: () => void;
};

const lightTheme: Theme = {
  background: '#F2F3F7',
  surface: '#FFFFFF',
  primary: '#6C63FF',
  primaryLight: '#E8E6FF',
  text: '#1A1A2E',
  textSecondary: '#6B7280',
  accent: '#FF6584',
  border: '#E5E7EB',
  tabBar: '#FFFFFF',
  tabBarBorder: '#E5E7EB',
  cardShadow: 'rgba(0,0,0,0.06)',
  inputBackground: '#F9FAFB',
  statusBar: 'dark',
  headerTint: '#1A1A2E',
};

const darkTheme: Theme = {
  background: '#0F0F23',
  surface: '#1A1A2E',
  primary: '#6C63FF',
  primaryLight: '#2A265E',
  text: '#EAEAFF',
  textSecondary: '#9CA3AF',
  accent: '#FF6584',
  border: '#2D2D4A',
  tabBar: '#1A1A2E',
  tabBarBorder: '#2D2D4A',
  cardShadow: 'rgba(0,0,0,0.3)',
  inputBackground: '#252542',
  statusBar: 'light',
  headerTint: '#EAEAFF',
};

const ThemeContext = createContext<ThemeContextType | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const systemScheme = useColorScheme();
  const [isDark, setIsDark] = useState(systemScheme === 'dark');

  const theme = useMemo(() => (isDark ? darkTheme : lightTheme), [isDark]);

  const toggleTheme = () => setIsDark(prev => !prev);

  return (
    <ThemeContext.Provider value={{ isDark, theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}
