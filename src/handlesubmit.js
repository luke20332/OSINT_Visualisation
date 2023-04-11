import React from "react";
import { datasref } from "./firestore";
import { useState } from "react";

function createNewData() {
    const [data, setData] = useState("")
    const createNewData = (e) => {
        e.preventDefault()
        const item = {
            task: data,
            done: false
        }
        datasref.push(item)
        setData("")
    }
    return (
        <form onSubmit={createNewData}>
            <input type="text" value={data} onChange={(e) => setData(e.target.value)} placeholder="create new data"></input>
        </form>
    )
}

export default createNewData