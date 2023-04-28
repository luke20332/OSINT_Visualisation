import React, {useRef, useState, useEffect } from "react";
import { StatusBar } from 'expo-status-bar';
import './index.css';
import Slider from '@react-native-community/slider';
import { StyleSheet, Text, View } from 'react-native';
import ids from './data/IDs.json';
import data from './data/joined_data.json';
import { fromUrl,fromArrayBuffer } from 'geotiff';
import Canvas from './canvas-component/canvas'
//import useOnDraw from './canvas-component/hooks'
import map from "./world.png"
// <img src={map} className="Map" alt="world map" class="center" />  

const DrawOnCanvas = React.forwardRef((props, ref) => {
  return (
    
      
      <canvas  width={1000}  height={500}  ref={ref}  className="CanvasOverlay" id= "my-canvas">
      </canvas>

  );
});





const idsRange = idsToDateRange();
const dateRange = dataRange();
var tiffReply = await loadTiff();
const bbox = tiffReply[0];
const width = tiffReply[1];
const height = tiffReply[2];

const scale = 16.2

// root of application
// write the HTML heere






export default function App() {
  const myref = useRef(null);

  function drawOnCanvas(color) {
    let ctx = myref.current.getContext("2d");
    ctx.fillStyle = color;
    const img = new Image()
    img.src = map
    img.onload = () => {
      ctx.drawImage(img, 0, 0)
      ctx.fillRect(100, 100, 32, 32);
    }
    
  }
  
  function callDrawOnCanvas(color) {
    drawOnCanvas(color);
  }

  function updateCanvas(value){
    sliderDataLoad(value)
    callDrawOnCanvas('red');

  }

  



  console.log("Starting App");
  console.log(bbox);




  


  const [range, setRange] = useState('1950');
  const [sliding, setSliding] = useState('');
  console.log("Finished App");



  return (
    
    <View style={styles.container}>
      
      <DrawOnCanvas ref={myref} />
      { }
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
        onSlidingComplete={value => updateCanvas(value)}

      />
      <StatusBar style = 'auto'/>
      <script type="text/javascript">
        
        const myCanvas = document.getElementById("my-canvas")
        const myContext = myCanvas.getContext("2d")
        myContext.drawImage(map,0,0)

      </script>
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
  var idsIndexs = {};
  for (var i = 0; i < idsRange.length; i++){
    var from = idsRange[i].from;
    var to = idsRange[i].to;
    if (value >= from && value <= to){
      const name = ids[i].title;
      if (! (idsIndexs.hasOwnProperty(name))){
        idsIndexs[name] = ids[i].cnt;
      }
    }
  } 
  //Print List of ids in range
  //console.log(idsIndexs);

  //For joined data
  //for each id get year 

  //Check data range
  //console.log(dateRange);
  var dataIndexs = [];
  const dataKeys = Object.keys(data);
  for (var i = 0; i < dateRange.length; i++){
    var date = dateRange[i].date;
    if (parseInt(date) == value){
      
      var deal = data[dataKeys[i]];
      //console.log(deal);
      var seller = deal.seller;
      var buyer = deal.buyer;
      dataIndexs.push({'id':dataKeys[i],'seller':seller, 'buyer':buyer});
    }
  }




  //Print List of data in range

  console.log("New function")
  //Testing new function on a single point located in Syndey
  const x = parseInt(getX(151)/scale); // 151 = Long
  const y = parseInt(getY(-33.8)/scale); //--33.8 = Lat
  console.log(x,y);


}

async function loadTiff(){

  const url = 'NE1_LR_LC.tif';
  const tiff = await fromUrl(url);
  console.log(tiff);
  const image = await tiff.getImage();
  const bbox = image.getBoundingBox();
  const x = image.getWidth();
  const y = image.getHeight();

  return [bbox, x, y];

}

function getX(longitude){
  const x = width * ((180+longitude) / 360);
  return x;
}
function getY(latitude){
  const y  = height * ((90-latitude) / 180);
  return y;
}