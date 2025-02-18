import { useParams } from "react-router-dom"
import { useEffect } from "react"
import { useItem } from "../context/ItemContext"
import { Model, UserGuitar } from "../types"

function Specs() {
    const { item, setItem } = useItem()
    const { modelName, serialNumber } = useParams()

    useEffect(() => {
        console.log("Effect triggered")
        console.log("Current item:", item)
        console.log("Params - Model:", modelName, "Serial:", serialNumber)
    
        if (!item && (modelName || serialNumber)) {
            const apiPath = serialNumber
                ? `/api/guitar/${serialNumber}`
                : `/api/model/${modelName}`
    
            console.log("Fetching from API:", apiPath)
    
            fetch(apiPath)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`)
                    }
                    return response.json()
                })
                .then((data: Model | UserGuitar) => {
                    console.log("Fetched data:", data)
                    setItem(data)
                })
                .catch(error => console.error("Error fetching item:", error))
        }
    }, [item, modelName, serialNumber, setItem])
    

    if (!item) return <p>Loading...</p>

    return (
        <div id="guitar-specs">
            {"serial_number" in item ? (
                <>
                    <h1>{item.serial_number}</h1>
                    <p>Model: {item.model ? item.model.model_name : "Unknown"}</p>
                </>
            ) : (
                <>
                    <h1>{item.model_name}</h1>
                    <p>Official Model</p>
                </>
            )}
        </div>
    );
}

export default Specs
