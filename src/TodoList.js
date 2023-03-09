import React, {useEffect, useState} from 'react'
// functiion component

export default function TodoList({ todos }) {
  return (
    <div>
      {todos.length}
    </div>
  )
}
