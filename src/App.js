import React, {useRef, useState, useEffect } from "react";
import {v4 as uuidv4} from 'uuid';
import map from "./wrld-15-crop.jpg"
import './index.css';


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

const LOCAL_STORAGE_KEY = 'todoApp.todos'


function App() {
  

  return (
    <>
      <img src={map} className="Map" alt="world map" class = "center" />
    </>
  )


}

export default App;
