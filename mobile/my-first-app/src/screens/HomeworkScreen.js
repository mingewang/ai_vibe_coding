import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  FlatList,
  Alert,
  Keyboard,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useTheme } from '../context/ThemeContext';

const PRIORITIES = ['Low', 'Medium', 'High'];

export default function HomeworkScreen() {
  const { theme } = useTheme();
  const [tasks, setTasks] = useState([
    { id: '1', title: 'Algebra Worksheet', subject: 'Math', priority: 'High', done: false },
    { id: '2', title: 'Lab Report', subject: 'Science', priority: 'Medium', done: false },
    { id: '3', title: 'Chapter 5 Reading', subject: 'History', priority: 'Low', done: true },
  ]);
  const [title, setTitle] = useState('');
  const [subject, setSubject] = useState('');
  const [priority, setPriority] = useState('Medium');
  const [showForm, setShowForm] = useState(false);

  const addTask = () => {
    if (!title.trim()) {
      Alert.alert('Error', 'Please enter a task title');
      return;
    }
    const newTask = {
      id: Date.now().toString(),
      title: title.trim(),
      subject: subject.trim() || 'General',
      priority,
      done: false,
    };
    setTasks([newTask, ...tasks]);
    setTitle('');
    setSubject('');
    setPriority('Medium');
    setShowForm(false);
    Keyboard.dismiss();
  };

  const toggleDone = (id) => {
    setTasks(tasks.map(t => (t.id === id ? { ...t, done: !t.done } : t)));
  };

  const deleteTask = (id) => {
    setTasks(tasks.filter(t => t.id !== id));
  };

  const priorityColor = (p) => {
    switch (p) {
      case 'High': return '#F87171';
      case 'Medium': return '#FBBF24';
      default: return '#34D399';
    }
  };

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={[styles.taskCard, { backgroundColor: theme.surface, borderLeftColor: priorityColor(item.priority) }]}
      onPress={() => toggleDone(item.id)}
      activeOpacity={0.7}
    >
      <View style={[styles.checkbox, item.done && { backgroundColor: theme.primary }]}>
        {item.done && <Ionicons name="checkmark" size={14} color="#FFF" />}
      </View>
      <View style={styles.taskInfo}>
        <Text style={[styles.taskTitle, { color: theme.text }, item.done && styles.taskDone]}>
          {item.title}
        </Text>
        <Text style={[styles.taskSubject, { color: theme.textSecondary }]}>{item.subject}</Text>
      </View>
      <TouchableOpacity onPress={() => deleteTask(item.id)} hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}>
        <Ionicons name="trash-outline" size={18} color={theme.textSecondary} />
      </TouchableOpacity>
    </TouchableOpacity>
  );

  return (
    <View style={[styles.container, { backgroundColor: theme.background }]}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: theme.text }]}>Homework Tracker</Text>
        <Text style={[styles.subtitle, { color: theme.textSecondary }]}>
          {tasks.filter(t => !t.done).length} remaining
        </Text>
      </View>

      {!showForm ? (
        <TouchableOpacity
          style={[styles.addButton, { backgroundColor: theme.primary }]}
          onPress={() => setShowForm(true)}
        >
          <Ionicons name="add-circle-outline" size={20} color="#FFF" />
          <Text style={styles.addButtonText}>Add Homework</Text>
        </TouchableOpacity>
      ) : (
        <View style={[styles.form, { backgroundColor: theme.surface }]}>
          <TextInput
            style={[styles.input, { backgroundColor: theme.inputBackground, color: theme.text, borderColor: theme.border }]}
            placeholder="Task title"
            placeholderTextColor={theme.textSecondary}
            value={title}
            onChangeText={setTitle}
          />
          <TextInput
            style={[styles.input, { backgroundColor: theme.inputBackground, color: theme.text, borderColor: theme.border }]}
            placeholder="Subject (optional)"
            placeholderTextColor={theme.textSecondary}
            value={subject}
            onChangeText={setSubject}
          />
          <View style={styles.priorityRow}>
            {PRIORITIES.map(p => (
              <TouchableOpacity
                key={p}
                style={[
                  styles.priorityBtn,
                  { borderColor: theme.border },
                  priority === p && { backgroundColor: priorityColor(p), borderColor: priorityColor(p) },
                ]}
                onPress={() => setPriority(p)}
              >
                <Text style={[styles.priorityText, { color: theme.textSecondary }, priority === p && { color: '#FFF' }]}>
                  {p}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
          <View style={styles.formActions}>
            <TouchableOpacity style={[styles.cancelBtn, { borderColor: theme.border }]} onPress={() => setShowForm(false)}>
              <Text style={[styles.cancelText, { color: theme.textSecondary }]}>Cancel</Text>
            </TouchableOpacity>
            <TouchableOpacity style={[styles.submitBtn, { backgroundColor: theme.primary }]} onPress={addTask}>
              <Text style={styles.submitText}>Add</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}

      <FlatList
        data={tasks}
        renderItem={renderItem}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.list}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
          <Text style={[styles.emptyText, { color: theme.textSecondary }]}>No homework yet — add one above!</Text>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, paddingHorizontal: 20, paddingTop: 60 },
  header: { marginBottom: 20 },
  title: { fontSize: 26, fontWeight: '800' },
  subtitle: { fontSize: 14, fontWeight: '500', marginTop: 2 },
  addButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 14,
    borderRadius: 14,
    marginBottom: 16,
  },
  addButtonText: { color: '#FFF', fontSize: 16, fontWeight: '700' },
  form: {
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  input: {
    borderRadius: 12,
    borderWidth: 1,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 15,
    marginBottom: 10,
  },
  priorityRow: { flexDirection: 'row', gap: 8, marginBottom: 14 },
  priorityBtn: {
    flex: 1,
    paddingVertical: 10,
    borderRadius: 10,
    borderWidth: 1,
    alignItems: 'center',
  },
  priorityText: { fontSize: 13, fontWeight: '600' },
  formActions: { flexDirection: 'row', gap: 10 },
  cancelBtn: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 12,
    borderWidth: 1,
    alignItems: 'center',
  },
  cancelText: { fontSize: 15, fontWeight: '600' },
  submitBtn: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: 'center',
  },
  submitText: { color: '#FFF', fontSize: 15, fontWeight: '700' },
  list: { paddingBottom: 100 },
  taskCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderRadius: 14,
    marginBottom: 10,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 1,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#D1D5DB',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  taskInfo: { flex: 1 },
  taskTitle: { fontSize: 15, fontWeight: '600' },
  taskDone: { textDecorationLine: 'line-through', opacity: 0.5 },
  taskSubject: { fontSize: 12, fontWeight: '500', marginTop: 2 },
  emptyText: { textAlign: 'center', marginTop: 40, fontSize: 15 },
});
