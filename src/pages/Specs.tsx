import { useParams } from "react-router-dom"
import { useEffect } from "react"
import { useItem } from "../context/ItemContext"
import { Model, UserGuitar } from "../types"

import SpecSheet from "../components/SpecSheet"

function Specs() {
    const { item, setItem } = useItem()
    const { modelName, serialNumber } = useParams()

    useEffect(() => {
        //details on page load (always trigger)
        console.log("Effect triggered")
        console.log("Current item:", item)
        console.log("Params - Model:", modelName, "Serial:", serialNumber)
    
        if (!item || isMismatch(item)) {
            const apiPath = serialNumber
                ? `/api/guitar/${serialNumber}`
                : `/api/model/${modelName}`
            
            //Retrieve guitar data (only trigger on refresh)
            console.log("Fetching from API:", apiPath)

            fetch(apiPath)
                .then(response => response.json())
                .then((data: Model | UserGuitar) => {
                    console.log("Fetched data:", data)
                    setItem(data)
                })
                .catch(error => console.error("Error fetching item:", error))
        }
    }, [modelName, serialNumber, setItem])

    function isMismatch(data: Model | UserGuitar) {
        if (serialNumber && "serial_number" in data) {
            return data.serial_number.toString() !== serialNumber
        }
        if (modelName && "model_name" in data) {
            return data.model_name !== modelName
        }
        return false
    }

    if (!item) return <p>Loading...</p>
    return (
        <div id="guitar-specs">
            <SpecSheet 
                item={item} 
                type={serialNumber ? "userGuitar" : "model"} 
            />
        </div>
    )
}

export default Specs
