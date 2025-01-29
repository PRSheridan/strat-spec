import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"

//explore is used for searching existing guitars by spec

function Explore () {
    const navigate = useNavigate()
    const [catalogue, setCatalogue] = useState<any[]>([])

    useEffect(() => {
        fetch('/guitars')
          .then((response) => response.json())
          .then((data) => {
            setCatalogue(data)
          })
      }, [])

    return (
        <>
            <div>User Submissions</div>
            {catalogue.map((item) => (
                <div key={item.id} className="item-card"
                    onClick={() => navigate(`/specs/${item.sn}`)}>
                    <div className="item-details">{item.name}</div>
                    <div className="item-details">{item.sn}</div>
                </div>
            ))}
        </>
    )
}

export default Explore