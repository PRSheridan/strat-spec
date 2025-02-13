import { useState, useEffect } from "react"
import GuitarCard from "../components/GuitarCard"
import { UserGuitar } from "../types"

function Guitars() {
    const [catalogue, setCatalogue] = useState<UserGuitar[]>([])

    // Fetches all UserGuitars and updates the catalogue
    useEffect(() => {
        fetch("/api/guitars")
            .then((response) => response.json())
            .then((data: UserGuitar[]) => {
                setCatalogue(data)
            })
            .catch((error) => console.error("Error fetching guitars:", error))
    }, [])
    
    // Map the UserGuitar data to individual GuitarCards
    return (
        <>
            <div>User Submitted Stratocasters</div>
            {catalogue.map((item) => (
                <GuitarCard key={item.id} item={item} />
            ))}
        </>
    );
}

export default Guitars
