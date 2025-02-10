import { useParams } from "react-router-dom"
import { useEffect, useState } from "react"
import { useGuitar } from "../context/GuitarContext"
import { Guitar } from "../types/Guitar"

function Specs() {
    const { serialNumber } = useParams()
    const { guitar } = useGuitar()
    const [fetchedGuitar, setFetchedGuitar] = useState<Guitar | null>(null)

    useEffect(() => {
        if (!guitar && serialNumber) {
            console.log(serialNumber)
            fetch(`/guitar/${serialNumber}`)
                .then((response) => response.json())
                .then((data: Guitar) => setFetchedGuitar(data))
                .catch((error) => console.error("Error fetching guitar:", error))
        }
    }, [guitar, serialNumber])

    const displayGuitar = guitar || fetchedGuitar

    return (
        <>
            {displayGuitar ? (
                <div>
                    <h1>{displayGuitar.name}</h1>
                    <p>Model: {displayGuitar.model.name} ({displayGuitar.model.years})</p>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </>
    )
}

export default Specs