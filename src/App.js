import TodoList from "./TodoList";
import React, {useEffect, useState } from "react";
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

function App() {
  const [todos, setTodos] = useState(['eat food', 'ie']) // empty array of todos
  // todos are props. passed to components, just like attributes to an elemnt

  return (
    <>
      <TodoList todos={todos}/> 
      <input type="Text"/>
      <button> Add Todo</button>
      <button> clear todos</button>
      <div>0 left to do</div>
    </>
  )


}

export default App;
