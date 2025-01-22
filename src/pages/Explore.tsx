import { useState } from "react";
import { useNavigate } from "react-router-dom"

function Explore () {
    const navigate = useNavigate()
    const [catalogue, setCatalogue] = useState([])
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