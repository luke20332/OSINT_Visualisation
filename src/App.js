import React, {useRef, useState, useEffect } from "react";
import { StatusBar } from 'expo-status-bar';
import map from "./NE1_LR_LC.png";
import './index.css';
import Slider from '@react-native-community/slider';
import { StyleSheet, Text, View } from 'react-native';
import ids from './data/IDs.json';
import data from './data/joined_data.json';
import { fromUrl } from 'geotiff';

const idsRange = idsToDateRange();
const dateRange = dataRange();
var bbox, width, height= await loadTiff();
//bbox[0] - Left/W
//bbox[1] - Bottom/S
//bbox[2] - Right/E
//bbox[3] - Top/N
const west = toRadians(bbox[0]);
const south = toRadians(bbox[1]);
const east = toRadians(bbox[2]);
const north = toRadians(bbox[3]);
//  REF https://stackoverflow.com/questions/41557891/convert-lat-long-to-x-y-position-within-a-bounding-box


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
  
  console.log("Starting App");
  console.log(bbox);





  const [range, setRange] = useState('1950');
  const [sliding, setSliding] = useState('');

  return (
    <View style={styles.container}>
      <img src = {map} className="Map" alt="world map" class = "center" />
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
        onSlidingComplete={value => sliderDataLoad(value)}

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


function idsToDateRange(){
  console.log("Starting ID parse");
  var dateRange = [];
  for (var i = 0; i < ids.length; i++){
    var from = ids[i].from;
    var to = ids[i].to;
    
    try{
      var fromYear = parseInt(from.substring(0,4));
    }catch(err){
      // eslint-disable-next-line no-redeclare
      var fromYear = 0;
    }

    try{
      var toYear = parseInt(to.substring(0,4));
    }catch(err){
      // eslint-disable-next-line no-redeclare
      var toYear = 0;
    }
    dateRange.push({'from':fromYear, 'to':toYear});
  }
  console.log("Finished ID parse");
  return dateRange;
}

function dataRange(){
  console.log("Starting data parse");

  const dataKeys = Object.keys(data);
  var dataRange = [];
  for (var i = 0; i < dataKeys.length; i++){
    var deal = data[dataKeys[i]];
    //console.log(deal);
    var date = deal['Order date'];
    //console.log(date);
    dataRange.push({'id':dataKeys[i],'date':date});
  
  }
  console.log("Finished data parse");
  return dataRange;

}


function sliderDataLoad(value){
  console.log(value);

  //Convert value to an int
  value = parseInt(value);


  //Check ids and combined data are loaded
  // console.log(ids);
  // console.log(data);

  //Check ids range
  //console.log(idsRange);

  //Find the correct ids index
  var idsIndexs = [];
  for (var i = 0; i < idsRange.length; i++){
    var from = idsRange[i].from;
    var to = idsRange[i].to;
    if (value >= from && value <= to){
      idsIndexs.push(i);
    }
  } 
  //Print List of ids in range
  //console.log(idsIndexs);

  //For joined data
  //for each id get year 

  //Check data range
  //console.log(dateRange);
  var dataIndexs = [];
  for (var i = 0; i < dateRange.length; i++){
    var date = dateRange[i].date;
    if (parseInt(date) == value){
      dataIndexs.push(i);
    }
  }

  //Print List of data in range
  //console.log(dataIndexs);

}

async function loadTiff(){

  const url = 'NE1_LR_LC.tif';
  const tiff = await fromUrl(url);
  const image = await tiff.getImage();
  const bbox = image.getBoundingBox();
  const x = image.getWidth();
  const y = image.getHeight();
  return [bbox, x, y];

}

function toRadians (deg) {
  return deg * (Math.PI/180);
}

function latLongToPixel(lat,long){
  lat = toRadians(lat);
  long = toRadians(long);
  const yMin = mecatorY(south);
  const yMax = mecatorY(north);
  const xFactor = width/(east-west);
  const yFactor = height/(yMax-yMin);

  var y = mecatorY(lat);
  var x = (long - west) * xFactor;
  y = (yMax - y) * yFactor;
  return [x,y];

}

function mecatorY(lat){
  return Math.log(Math.tan(Math.PI/4 + lat/2));
}