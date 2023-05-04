import React, {useRef, useState, useEffect } from "react";
import { StatusBar } from 'expo-status-bar';
import './index.css';
import Slider from '@react-native-community/slider';
import { StyleSheet, Text, View } from 'react-native';


import { fromUrl,fromArrayBuffer } from 'geotiff';
import Canvas from './canvas-component/canvas'
//import useOnDraw from './canvas-component/hooks'
import map from "./world.png"
// <img src={map} className="Map" alt="world map" class="center" />  

const ids = require('./data/IDS.json');
const data = require('./data/joined_data.json');

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

  function drawOnCanvas(data) {
    let ctx = myref.current.getContext("2d");
    ctx.fillStyle = 'red';
    const img = new Image()
    img.src = map
    img.onload = () => {

      ctx.drawImage(img, 0, 0)
      console.log("Drawing Image")
      console.log(data)
      //Lines
      for (var i = 0; i < data.length; i++){
        var xS = data[i].xS;
        var yS = data[i].yS;

        var xB = data[i].xB;
        var yB = data[i].yB;

        drawArrow(ctx, xS, yS, xB, yB, 2, 'black');

        
      }
      //Points
      for (var i = 0; i < data.length; i++){
        var xS = data[i].xS;
        var yS = data[i].yS;

        var xB = data[i].xB;
        var yB = data[i].yB;
        ctx.fillRect(xS-5, yS-5, 10,10);
        ctx.fillRect(xB-5, yB-5, 10, 10);
      }
    }
    
  }
  
  function callDrawOnCanvas(data) {
    drawOnCanvas(data);
  }

  function updateCanvas(value){
    var data = sliderDataLoad(value);
    callDrawOnCanvas(data);
    updateTable(data);

  }

  function updateTable(data){
    var html =`
    <table border='1' style='border-collapse:collapse'>
    <thead>
      <tr>
        <th>Seller</th>
        <th>Buyer</th>
      </tr>
    </thead>
    
    <tbody>
    `;
    for (var i = 0; i < data.length; i++){
      html += `
      <tr>
      <td style='text-align: center'>${data[i].seller}</td>
      <td style='text-align: center'>${data[i].buyer}</td>
      </tr>
      `;
    }
    html += `
    </tbody>
    </table>
    `;
    document.getElementsByClassName("data")[0].innerHTML = html;



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
        //onSlidingStart={() => setSliding('Calculating...')}
        onSlidingComplete={value => updateCanvas(value)}

      />
      <StatusBar style = 'auto'/>
      Select a year using the slider above to get started
      <p></p>
      After selcting a year, the map will display the arms trade for that year as well as a table of these below
      <p></p>
      Please note that only countries are displayed, and of these only ones that we have the geographic mapping for
      <p></p>

      <div className="data"></div>
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
  var dataOut = [];
  const dataKeys = Object.keys(data);
  for (var i = 0; i < dateRange.length; i++){
    var date = dateRange[i].date;
    if (parseInt(date) == value){
      
      var deal = data[dataKeys[i]];
      console.log(deal);
      var seller = deal.Seller;
      var buyer = deal.Buyer;
      console.log(seller);
      var cnt = idsIndexs[seller];
      if (cnt == undefined){
        continue;
      }
      var long = cnt[0];
      var lat = cnt[1];
      var xS = parseInt(getX(long)/scale);
      var yS = parseInt(getY(lat)/scale); 
      cnt = idsIndexs[buyer];
      if (cnt == undefined){
        continue;
      }
      long = cnt[0];
      lat = cnt[1];
      var xB = parseInt(getX(long)/scale);
      var yB = parseInt(getY(lat)/scale);
    
      dataOut.push({'id':dataKeys[i],'seller':seller, 'buyer':buyer, 'xS':xS, 'yS':yS, 'xB':xB, 'yB':yB});
      


    }
  }




  //Print List of data in range

  //console.log("New function")
  //Testing new function on a single point located in Syndey
  //const x = parseInt(getX(151)/scale); // 151 = Long
  //const y = parseInt(getY(-33.8)/scale); //--33.8 = Lat
  //console.log(x,y);
  return dataOut;

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

//https://codepen.io/chanthy/pen/WxQoVG
function drawArrow(ctx, fromx, fromy, tox, toy, arrowWidth, color){
  //variables to be used when creating the arrow
  var headlen = 10;
  var angle = Math.atan2(toy-fromy,tox-fromx);

  ctx.save();
  ctx.strokeStyle = color;

  //starting path of the arrow from the start square to the end square
  //and drawing the stroke
  ctx.beginPath();
  ctx.moveTo(fromx, fromy);
  ctx.lineTo(tox, toy);
  ctx.lineWidth = arrowWidth;
  ctx.stroke();

  //starting a new path from the head of the arrow to one of the sides of
  //the point
  ctx.beginPath();
  ctx.moveTo(tox, toy);
  ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),
             toy-headlen*Math.sin(angle-Math.PI/7));

  //path from the side point of the arrow, to the other side point
  ctx.lineTo(tox-headlen*Math.cos(angle+Math.PI/7),
             toy-headlen*Math.sin(angle+Math.PI/7));

  //path from the side point back to the tip of the arrow, and then
  //again to the opposite side point
  ctx.lineTo(tox, toy);
  ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),
             toy-headlen*Math.sin(angle-Math.PI/7));

  //draws the paths created above
  ctx.stroke();
  ctx.restore();
}