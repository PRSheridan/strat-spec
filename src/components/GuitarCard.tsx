import { useNavigate } from 'react-router-dom'
import { useGuitar } from '../context/GuitarContext'
import { UserGuitar, Model } from '../types'

interface GuitarCardProps {
    item: UserGuitar | Model
    viewMode: 'compact' | 'detailed'
}

function GuitarCard({ item, viewMode }: GuitarCardProps) {
    const { setGuitar } = useGuitar()
    const navigate = useNavigate()

    function handleSelectItem(item: UserGuitar | Model) {
        if ('serial_number' in item) {
            setGuitar(item)
            navigate(`/specs/${item.serial_number}`)
        } else {
            navigate(`/models/${item.model_name}`)
        }
    }

    const isUserGuitar = 'serial_number' in item

    return (
        <div key={item.id} className={`guitar-card ${viewMode}`} onClick={() => handleSelectItem(item)}>            
            <div className="item-name">
                {isUserGuitar ? `SN: ${item.serial_number}` : item.model_name}
            </div>


            <img className="guitar-image" 
                 src={''} 
                 alt={isUserGuitar ? `SN: ${item.serial_number}` : item.model_name} />

            <div className="item-details">
                {viewMode === 'detailed' ? (
                    isUserGuitar ? (
                        <>
                            <div>Year: {item.year}</div>
                            <div>Country: {item.country}</div>
                            <div>Owner: {item.owner.username}</div>
                            <div>Wood: {item.body.wood}</div>
                            <div>Finish: {item.body.finish}</div>
                            <div>Pickups: {item.pickup_configuration}</div>
                        </>
                    ) : (
                        <>
                            <div>Years: {item.year_range}</div>
                            <div>Country: {item.country}</div>
                            <div>Body Wood: {item.body.wood}</div>
                            <div>Neck Wood: {item.neck.wood}</div>
                            <div>Fretboard: {item.fretboard.material}</div>
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





