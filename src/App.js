import TodoList from "./TodoList";
import React, {useRef, useState, useEffect } from "react";
import {v4 as uuidv4} from 'uuid';

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
  const [todos, setTodos] = useState([]) // empty array of todos
  // todos are props. passed to components, just like attributes to an element

  const todoNameRef = useRef()


  useEffect(()=> {
    const storedTodos = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY))
    if (storedTodos) {
      setTodos(storedTodos)
    }
  }, [])

  // call upon a change
  useEffect(() => {
    
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(todos))
  }, [todos])

  // checking the todos yes or no

  function toggleTodo(id){
    const newTodos = [...todos] // create copy first before setting state var
    const todo = newTodos.find(todo => todo.id === id)
    todo.complete = !todo.complete
    setTodos(newTodos)

  }

  function handleAddTodo(e){
    const name = todoNameRef.current.value

    if (name === '') return 
    
    setTodos(prevTodos => {
      return [...prevTodos, {id: uuidv4(), name: name, complete:false}]
    })
    todoNameRef.current.value = null
  }
  // to access what was typed, use useRef hook, to reference elements in html

  function handleClearTodos(){
    const newTodos = todos.filter(todo => !todo.complete)
    setTodos(newTodos)
    
  }

  return (
    <>
      <TodoList todos={todos} toggleTodo = {toggleTodo}/> 
      <input ref = {todoNameRef} type="text"/>
      <button onClick={handleAddTodo}> Add Todo</button>
      <button onClick = {handleClearTodos}> clear todos</button>
      <div>{todos.filter(todo => !todo.complete).length} left to do</div>
    </>
  )


}

export default App;
