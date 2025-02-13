import { useNavigate } from "react-router-dom"
import { useGuitar } from "../context/GuitarContext"
import { UserGuitar, Model } from "../types"

// an item can be either a UserGuitar or a Guitar Model
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
            navigate(`/models/${item.model_name}`)
        }
    }

    const isUserGuitar = "serial_number" in item

    return (
        <div key={item.id} className="guitar-card" onClick={() => handleSelectItem(item)}>
            {isUserGuitar ? 
                <div className="item-details">
                    <div>Serial Number: {item.serial_number}</div>
                    <div>Year: {item.year}</div>
                    <div>Country: {item.country}</div>
                    <div>Owner: {item.owner.username}</div>
                </div>
            : 
                <div className="item-details">
                    <div>Model: {item.model_name}</div>
                    <div>Years: {item.year_range}</div>
                    <div>Country: {item.country}</div>
                </div>
            }
        </div>
    )
}

export default GuitarCard


