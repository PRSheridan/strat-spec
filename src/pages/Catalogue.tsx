import { useState, useEffect } from "react"
import CatalogueItem from "../components/GuitarCard"
import { UserGuitar } from "../types"

function Explore() {
    const [catalogue, setCatalogue] = useState<UserGuitar[]>([])

    useEffect(() => {
        fetch("/api/guitars")
            .then((response) => response.json())
            .then((data: UserGuitar[]) => {
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
