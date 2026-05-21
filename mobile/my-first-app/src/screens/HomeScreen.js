import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useTheme } from '../context/ThemeContext';

export default function HomeScreen() {
  const { theme, isDark, toggleTheme } = useTheme();
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);

  const quickStats = [
    { label: 'Pending', value: 4, color: theme.primary, icon: 'time-outline' },
    { label: 'Completed', value: 12, color: '#34D399', icon: 'checkmark-circle-outline' },
    { label: 'Overdue', value: 1, color: '#F87171', icon: 'alert-circle-outline' },
  ];

  return (
    <ScrollView style={[styles.container, { backgroundColor: theme.background }]}>
      <View style={styles.header}>
        <View>
          <Text style={[styles.greeting, { color: theme.textSecondary }]}>Welcome back</Text>
          <Text style={[styles.title, { color: theme.text }]}>My Dashboard</Text>
        </View>
        <TouchableOpacity
          style={[styles.avatar, { backgroundColor: theme.primaryLight }]}
          onPress={toggleTheme}
        >
          <Ionicons name={isDark ? 'sunny' : 'moon'} size={22} color={theme.primary} />
        </TouchableOpacity>
      </View>

      <View style={[styles.statsRow, { backgroundColor: theme.surface }]}>
        {quickStats.map((stat, index) => (
          <View
            key={stat.label}
            style={[
              styles.statCard,
              index < quickStats.length - 1 && { borderRightWidth: 1, borderRightColor: theme.border },
            ]}
          >
            <View style={[styles.statIconWrap, { backgroundColor: stat.color + '18' }]}>
              <Ionicons name={stat.icon} size={22} color={stat.color} />
            </View>
            <Text style={[styles.statValue, { color: theme.text }]}>{stat.value}</Text>
            <Text style={[styles.statLabel, { color: theme.textSecondary }]}>{stat.label}</Text>
          </View>
        ))}
      </View>

      <View style={[styles.card, { backgroundColor: theme.surface }]}>
        <View style={styles.cardHeader}>
          <Ionicons name="notifications-outline" size={20} color={theme.primary} />
          <Text style={[styles.cardTitle, { color: theme.text }]}>Notifications</Text>
        </View>
        <View style={styles.settingRow}>
          <Text style={[styles.settingLabel, { color: theme.text }]}>Push Notifications</Text>
          <Switch
            value={notificationsEnabled}
            onValueChange={setNotificationsEnabled}
            trackColor={{ false: theme.border, true: theme.primaryLight }}
            thumbColor={notificationsEnabled ? theme.primary : '#9CA3AF'}
          />
        </View>
      </View>

      <View style={[styles.card, { backgroundColor: theme.surface }]}>
        <View style={styles.cardHeader}>
          <Ionicons name="calendar-outline" size={20} color={theme.primary} />
          <Text style={[styles.cardTitle, { color: theme.text }]}>Upcoming Deadlines</Text>
        </View>
        {['Math HW - Due Tomorrow', 'Science Project - Due Fri', 'History Essay - Due Next Mon'].map(
          (item, i) => (
            <View key={i} style={[styles.deadlineRow, i > 0 && { borderTopWidth: 1, borderTopColor: theme.border }]}>
              <View style={[styles.dot, { backgroundColor: i === 0 ? theme.accent : theme.primary }]} />
              <Text style={[styles.deadlineText, { color: theme.text }]}>{item}</Text>
            </View>
          )
        )}
      </View>

      <TouchableOpacity style={[styles.fab, { backgroundColor: theme.primary }]}>
        <Ionicons name="add" size={28} color="#FFF" />
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, paddingHorizontal: 20, paddingTop: 60 },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  greeting: { fontSize: 14, fontWeight: '500' },
  title: { fontSize: 26, fontWeight: '800', marginTop: 2 },
  avatar: {
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
  },
  statsRow: {
    flexDirection: 'row',
    borderRadius: 16,
    paddingVertical: 18,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  statCard: { flex: 1, alignItems: 'center' },
  statIconWrap: {
    width: 42,
    height: 42,
    borderRadius: 21,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  statValue: { fontSize: 22, fontWeight: '800' },
  statLabel: { fontSize: 12, fontWeight: '500', marginTop: 2 },
  card: {
    borderRadius: 16,
    padding: 18,
    marginBottom: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 14,
  },
  cardTitle: { fontSize: 16, fontWeight: '700' },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  settingLabel: { fontSize: 15, fontWeight: '500' },
  deadlineRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    gap: 10,
  },
  dot: { width: 8, height: 8, borderRadius: 4 },
  deadlineText: { fontSize: 14, fontWeight: '500' },
  fab: {
    position: 'absolute',
    right: 0,
    bottom: 20,
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#6C63FF',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
});
