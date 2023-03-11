import React, {useEffect, useState} from 'react'
import Todo from './Todo'
// functiion component

export default function TodoList({ todos, toggleTodo }) {
  return (
    todos.map(todo =>{
      return <Todo key = {todo.id} toggleTodo={toggleTodo} todo = {todo} />
    }) 
    
    
    
    
    // todos is a list, and map loops over all the elemtns and returns the individual elements inside it

    // error as there are no individual keys for the todos, so react rerenders each time.
    // rerender ones which change

    // key is the name of the todo, ie eat food. now theyre unique, they only rerender unique elemtents

  )
}
