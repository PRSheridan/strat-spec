import { useNavigate } from "react-router-dom"
import { useGuitar } from "../context/GuitarContext"
import { UserGuitar, Model } from "../types"

interface GuitarCardProps {
    item: UserGuitar | Model
}

function GuitarCard({ item }: GuitarCardProps) {
    const { setGuitar } = useGuitar()
    const navigate = useNavigate()

    function handleSelectItem(item: UserGuitar | Model) {
        if ("serial_number" in item) {
            setGuitar(item)
            navigate(`/specs/${item.serial_number}`)
        } else {
            navigate(`/models/${item.id}`)
        }
    }

    const isUserGuitar = "serial_number" in item
    const modelName = "model_name" in item ? item.model_name : item.model?.model_name || "Unknown Model"
    const serialNumber = isUserGuitar ? item.serial_number : "Model"

    return (
        <div key={item.id} className="guitar-card" onClick={() => handleSelectItem(item)}>
            <div className="item-details">{modelName}</div>
            {isUserGuitar && <div className="item-details">{serialNumber}</div>}
        </div>
    )
}

export default GuitarCard


