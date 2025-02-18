import { useState, useEffect } from 'react';
import GuitarCard from '../components/GuitarCard';
import { Model, UserGuitar } from '../types';

interface ListProps {
    type: 'models' | 'guitars';
}

// List the items based on the URL. 
// Models nad Guitars have slightly different displays handled by the GuitarCard
//

function List({ type }: ListProps) {
    const [items, setItems] = useState<(Model | UserGuitar)[]>([]);
    const [viewMode, setViewMode] = useState<'compact' | 'detailed'>('detailed');

    useEffect(() => {
        setItems([])
        fetch(`/api/${type}`)
            .then(response => response.json())
            .then((data: (Model | UserGuitar)[]) => setItems(data))
            .catch(error => console.error(`Error fetching ${type}:`, error));
    }, [type]);

    return (
        <>
            <div className="header-container">
                <div className="page-name">
                    {type === 'models' ? 'Stratocaster Models' : 'User Submitted Stratocasters'}
                </div>
                <button
                    className="toggle-view-btn"
                    onClick={() => setViewMode(viewMode === 'compact' ? 'detailed' : 'compact')}
                >
                    {viewMode === 'compact' ? 'Switch to Detailed View' : 'Switch to Compact View'}
                </button>
            </div>

            <div className="list-container">
                {items.map(item => (
                    <GuitarCard key={item.id} item={item} viewMode={viewMode} />
                ))}
            </div>
        </>
    );
}

export default List;
