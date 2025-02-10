import { useState, useEffect } from "react"
import CatalogueItem from "../components/CatalogueItem"
import { Guitar } from "../types/Guitar"

function Explore() {
    const [catalogue, setCatalogue] = useState<Guitar[]>([])

    useEffect(() => {
        fetch("/guitars")
            .then((response) => response.json())
            .then((data: Guitar[]) => {
                setCatalogue(data)
            })
            .catch((error) => console.error("Error fetching guitars:", error))
    }, [])

    return (
        <>
            <div>User Submissions</div>
            {catalogue.map((item) => (
                <CatalogueItem key={item.id} item={item} />
            ))}
        </>
    );
}

export default Explore
