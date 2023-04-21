import React, {useRef, useState, useEffect } from "react";
import { StatusBar } from 'expo-status-bar';
import map from "./wrld-15-crop.jpg"
import './index.css';
import Slider from '@react-native-community/slider';
import { StyleSheet, Text, View } from 'react-native';
import Canvas from './canvas-component/canvas'


// root of application
// write the HTML heere

// react manages state, if state chanes, it rerenders
// redner to dos, so if anythign changes, it rerenders.

// use state hook
// const []
// useState returns an array
// first element is the list of todos 
// second element is the function which changes the todos
// object destructuring

// todos = all the todos in the state
// settodos = what we use to change the,




export default function App() {
  
  const [range, setRange] = useState('1950');
  const [sliding, setSliding] = useState('');

  

  return (
    <View style={styles.container}>
      <img src={map} className="Map" alt="world map" class = "center" />
      <Text style={{ fontSize:20, fontWeight: 'bold' }}>{range}</Text>
      <Text style={{ fontSize:20, fontWeight: 'bold' }}>{sliding}</Text>
      <Canvas 
        width={700}
        height={500}
      />

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
        onSlidingComplete={console.log(value)}

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

//export default App;
