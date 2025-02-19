export interface User {
    id: number;
    username: string;
    email: string;
    role: string;
    user_guitars: UserGuitar[];
}

export interface Model {
    id: number;
    brand: string;
    model_name: string;
    year_range: string;
    country: string;
    scale_length: number;
    relic: string;
    other_controls: string;
    hardware_finish: string[]; 
    pickup_configuration: string[];

    pickups: GuitarPickup[];
    bodies: Body[];
    fretboards: Fretboard[];
    pickguards: Pickguard[];
    switches: Switch[];
    controls: Controls[];

    neck: Neck;
    headstock: Headstock;
    nut: Nut;
    frets: Frets;
    inlays: Inlays;
    bridge: Bridge;
    saddles: Saddles;
    tuning_machine: TuningMachine;
    string_tree: StringTree;
    neck_plate: NeckPlate;
    
}

export interface UserGuitar {
    id: number;
    brand: string;
    name: string;
    serial_number: string;
    serial_number_location: string;
    year: number;
    country: string;
    weight: string;
    scale_length: number;
    other_controls: string;
    hardware_finish: string;
    relic: string;
    modified: boolean;
    modifications: string;
    pickup_configuration: string;

    pickups: GuitarPickup[];
    owner: User;
    model?: Model | null;
    
    body: Body;
    fretboard: Fretboard;
    pickguard: Pickguard;
    switch: Switch;
    controls: Controls;
    
    neck: Neck;
    headstock: Headstock;
    nut: Nut;
    frets: Frets;
    inlays: Inlays;
    bridge: Bridge;
    saddles: Saddles;
    tuning_machine: TuningMachine;
    string_tree: StringTree;
    neck_plate: NeckPlate;
    
}

export interface GuitarPickup {
    id: number;
    guitar: UserGuitar | Model;
    pickup: Pickup;
    position: "Neck" | "Middle" | "Bridge" | "Any";
}

export interface Pickup {
    id: number;
    brand: string;
    model: string; 
    position: string[];
    type: string; 
    magnet: string; 
    resistance: number;
    inductance: number;
    active: boolean;
    noiseless: boolean;
    staggered_poles: boolean;
    wax_potted: boolean;
    cover: string;
}

export interface Body {
    id: number;
    wood: string;
    contour: string;
    routing: string;
    chambering: boolean;
    binding: boolean;
    finish: string;
    color: string;
}

export interface Neck {
    id: number;
    wood: string;
    finish: string;
    shape: string;
    scale_length: number;
    truss_rod: string;
}

export interface Headstock {
    id: number;
    shape: string;
    decal_style: string;
    reverse: boolean;
}

export interface Fretboard {
    id: number;
    material: string;
    radius: number;
    fret_count: number;
    binding: boolean;
    scalloped: boolean;
}

export interface Frets {
    id: number;
    material: string;
    size: string;
}

export interface Nut {
    id: number;
    width: number;
    material: string;
    locking: boolean;
}

export interface Inlays {
    id: number;
    shape: string;
    material: string;
    spacing: string;
}

export interface Bridge {
    id: number;
    model: string;
    screws: number;
    spacing: number;
    tremolo: boolean;
}

export interface Saddles {
    id: number;
    style: string;
    material: string;
}

export interface Switch {
    id: number;
    positions: number;
    color: string;
}

export interface Controls {
    id: number;
    configuration: string;
    color: string;
}

export interface TuningMachine {
    id: number;
    model: string;
    locking: boolean;
}

export interface StringTree {
    id: number;
    model: string;
    count: number;
}

export interface NeckPlate {
    id: number;
    style: string;
    bolts: number;
}

export interface Pickguard {
    id: number;
    ply_count: number;
    screws: number;
    configuration: string;
    color: string;
}
