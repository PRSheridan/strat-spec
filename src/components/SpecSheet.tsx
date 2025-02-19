import { Model, UserGuitar } from "../types";

interface SpecSheetProps {
    item: Model | UserGuitar;
    type: "model" | "userGuitar";
}

function SpecSheet({ item, type }: SpecSheetProps) {
    if (type === "model") {
        const model = item as Model;
        return (
            <>
            <h1>{model.model_name}</h1>
            <div className="spec-sheet-header">
                <p>Country: {model.country}</p>
                <p>Year Range: {model.year_range}</p>
            </div>
            <div className="spec-sheet-about">
                space for accurate description of the model
            </div>
            <div className="spec-sheet">
                <div className="spec-sheet-sub">
                    <h2>Electronics</h2>
                    <p>Pickup Configuration: {model.pickup_configuration}</p>
                    <p>Other Controls: {model.other_controls || "None"}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Finish & Hardware</h2>
                    <p>Hardware Finish: {model.hardware_finish}</p>
                    <p>Relic: {model.relic || "None"}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Body</h2>
                    <p>Wood: </p>
                    <p>Finish: </p>
                    <p>Color: </p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Neck & Fretboard</h2>
                    <p>Neck Wood: {model.neck.wood}</p>
                    <p>Neck Shape: {model.neck.shape}</p>
                    <p>Scale Length: {model.neck.scale_length} inches</p>
                    <p>Fretboard Material: </p>
                    <p>Fretboard Radius: </p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Bridge & Pickguard</h2>
                    <p>Bridge Model: {model.bridge.model}</p>
                    <p>Bridge Spacing: {model.bridge.spacing} mm</p>
                    <p>Pickguard Ply Count: </p>
                    <p>Pickguard Color: </p>
                </div>
            </div>
            <div>pictures here</div>
            </>
        );
    } else {
        const guitar = item as UserGuitar;
        return (
            <>
            <h1>{guitar.name}</h1>
            <div className="spec-sheet-header">
                <p>Serial Number: {guitar.serial_number}</p>
                <p>Owner: {guitar.owner.username}</p>
                <p>Country: {guitar.country}</p>
                <p>Year: {guitar.year}</p>
            </div>
            <div className="spec-sheet-about">
                space for an owner to include details about their guitar
            </div>
            <div className="spec-sheet">
                <div className="spec-sheet-sub">
                    <h2>Ownership & Customization</h2>
                    <p>Serial Number Location: {guitar.serial_number_location}</p>
                    <p>Weight: {guitar.weight} lbs</p>
                    <p>Modified: {guitar.modified ? "Yes" : "No"}</p>
                    {guitar.modified && <p>Modifications: {guitar.modifications}</p>}
                    {guitar.model && <p>Based on Model: {guitar.model.model_name}</p>}
                </div>

                <div className="spec-sheet-sub">
                    <h2>Electronics</h2>
                    <p>Pickup Configuration: {guitar.pickup_configuration}</p>
                    <p>Other Controls: {guitar.other_controls || "None"}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Finish & Hardware</h2>
                    <p>Hardware Finish: {guitar.hardware_finish}</p>
                    <p>Relic: {guitar.relic || "None"}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Body</h2>
                    <p>Wood: {guitar.body.wood}</p>
                    <p>Finish: {guitar.body.finish}</p>
                    <p>Color: {guitar.body.color}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Neck & Fretboard</h2>
                    <p>Neck Wood: {guitar.neck.wood}</p>
                    <p>Neck Shape: {guitar.neck.shape}</p>
                    <p>Scale Length: {guitar.neck.scale_length} inches</p>
                    <p>Fretboard Material: {guitar.fretboard.material}</p>
                    <p>Fretboard Radius: {guitar.fretboard.radius} inches</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Bridge & Pickguard</h2>
                    <p>Bridge Model: {guitar.bridge.model}</p>
                    <p>Bridge Spacing: {guitar.bridge.spacing} mm</p>
                    <p>Pickguard Ply Count: {guitar.pickguard.ply_count}</p>
                    <p>Pickguard Color: {guitar.pickguard.color}</p>
                </div>
            </div>
            <div>pictures here</div>
            </>
        );
    }
}

export default SpecSheet;
