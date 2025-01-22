import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function SearchForm () {
    const navigate = useNavigate()
    const [SN, setSN] = useState("")

    function handleSubmit(e: any) {
      e.preventDefault()
      console.log(SN)
      navigate(`/specs/${SN}`)
    }

    return (
        <div id="search-form">
        <form onSubmit={handleSubmit}>
            <input 
              type="text"
              value={SN}
              onChange={(e) => setSN(e.target.value)} />
            <input type="submit" />
        </form>
        <p>Enter your Stratocaster's serial number above and hit enter</p>
      </div>
    )
}

export default SearchForm