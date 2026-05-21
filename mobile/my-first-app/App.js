import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { Button, Alert } from "react-native";

export default function HomeScreen() {
  return (
    <View style={{ padding: 40 }}>
      <Text style={{ fontSize: 30 }}>
        My First App
      </Text>

      <Button
        title="Click Me"
        onPress={() => Alert.alert("Hello!")}
      />
    </View>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
