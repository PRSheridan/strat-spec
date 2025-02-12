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
            fetch(`/api/guitar/${serialNumber}`)
                .then((response) => response.json())
                .then((data: Guitar) => setFetchedGuitar(data))
                .catch((error) => console.error("Error fetching guitar:", error))
        }
    }, [guitar, serialNumber])

    const displayGuitar = guitar || fetchedGuitar
    console.log(displayGuitar)
    return (
        <>
            {displayGuitar ? (
                <div id="guitar-specs">
                    <h1>{displayGuitar.serial_number}</h1>
                    <p>Model: {displayGuitar.model.model_name}</p>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </>
    )
}

export default Specs