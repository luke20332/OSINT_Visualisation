import React, {useRef, useState, useEffect } from "react";
import { StatusBar } from 'expo-status-bar';
import './index.css';
import Slider from '@react-native-community/slider';
import { StyleSheet, Text, View } from 'react-native';
import Canvas from './canvas-component/canvas'




export default function App() {
  
  const [range, setRange] = useState('1950');
  const [sliding, setSliding] = useState('');

  

  return (
    <View style={styles.container}>
      <Canvas 
        width={900}
        height={750}
      />
      <Text style={{ fontSize:20, fontWeight: 'bold' }}>{range}</Text>
      <Text style={{ fontSize:20, fontWeight: 'bold' }}>{sliding}</Text>

      <Slider
        style={{ width:1000, height: 40}}
        minimumValue = {1950}
        maximumValue = {2022}
        minimumTrackTintColor = 'tomato'
        maximumTrackTintColor = '#000'
        thumbTintColor = 'tomato'
        value = {1950}
        onValueChange = {value => setRange(parseInt(value))}
        onSlidingStart={() => setSliding('Calculating...')}
        onSlidingComplete={value => console.log(value)}

      />
      <StatusBar style = 'auto'/>
    </View>
  );


}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center'
  }
});