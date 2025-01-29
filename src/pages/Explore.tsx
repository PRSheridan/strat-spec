import { useState, useEffect } from "react";

import CatalogueItem from '../components/CatalogueItem'

//explore is used for searching existing guitars by spec

function Explore () {
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
                <CatalogueItem item={item}/>
            ))}
        </>
    )
}

export default Explore