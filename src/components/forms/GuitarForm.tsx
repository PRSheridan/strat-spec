import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {useForm, SubmitHandler} from "react-hook-form"
import { UserGuitar } from "../../types";

function GuitarForm () {
    const navigate = useNavigate()
    const [SN, setSN] = useState("")

    function handleSubmit(e: any) {
      e.preventDefault()
      navigate(`/specs/${SN}`)
    }

    return (
        <div id="search-form">
        <form onSubmit={handleSubmit}>
            <input 
              type="text"
              value={SN}
              onChange={(e) => setSN(e.target.value)} />
            <input type="submit" value="Search"/>
        </form>
        <p>Enter your Stratocaster's serial number above.</p>
      </div>
    )
}

export default GuitarForm