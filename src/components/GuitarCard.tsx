import { useNavigate } from 'react-router-dom'
import { useItem } from '../context/ItemContext'
import { UserGuitar, Model } from '../types'

interface GuitarCardProps {
    item: UserGuitar | Model
    viewMode: 'compact' | 'detailed'
}

function GuitarCard({ item, viewMode }: GuitarCardProps) {
    const { setItem } = useItem()
    const navigate = useNavigate()

    function handleSelectItem(item: UserGuitar | Model) {
        setItem(item)
        if ('serial_number' in item) {
            navigate(`/guitar/${item.serial_number}`)
        } else {
            navigate(`/model/${item.model_name.replace(" ", "_")}`)
        }
    }

    const isUserGuitar = 'serial_number' in item

    return (
        <div key={item.id} className={`guitar-card ${viewMode}`} onClick={() => handleSelectItem(item)}>    

            <img className="guitar-image" 
                 src='./src/assets/my85buqmt4reuv01rcsp.jpg'
                 alt={isUserGuitar ? item.name : item.model_name} />    

            <div className="item-name">
                {isUserGuitar ? item.name : item.model_name}
            </div>
  
            <div className="item-details">
                {viewMode === 'detailed' ? (
                    isUserGuitar ? (
                        <>
                            <div>Serial Number: {item.serial_number}</div>
                            <div>Year: {item.year}</div>
                            <div>Country: {item.country}</div>
                            <div>Owner: {item.owner.username}</div>
                        </>
                    ) : (
                        <>
                            <div>Years: {item.year_range}</div>
                            <div>Country: {item.country}</div>
                            <div>Body Wood: {item.bodies.map((body) => body.wood).join(", ")}</div>
                            <div>Fretboard: {item.fretboards.map((fretboard) => fretboard.material).join(", ")}</div>
                            <div>Bridge: {item.bridge.model}</div>
                            <div>Pickups: {item.pickup_configuration}</div>
                        </>
                    )
                ) : null}
            </div>
        </div>
    )
}

export default GuitarCard





