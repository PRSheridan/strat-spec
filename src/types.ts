export interface Model {
    id: number;
    model_name: string;
    year_range: string;
    country: string;
    pickup_configuration: string;
    other_controls: string;
    hardware_finish: string;
    relic: string;

    body: Body;
    neck: Neck;
    headstock: Headstock;
    fretboard: Fretboard;
    nut: Nut;
    frets: Frets;
    inlays: Inlays;
    bridge: Bridge;
    saddles: Saddles;
    switch: Switch;
    controls: Controls;
    tuning_machine: TuningMachine;
    string_tree: StringTree;
    neck_plate: NeckPlate;
    pickguard: Pickguard;
}

export interface UserGuitar {
    name: string;
    id: number;
    serial_number: number;
    serial_number_location: string;
    year: string;
    country: string;
    weight: number;
    pickup_configuration: string;
    other_controls: string;
    hardware_finish: string;
    modified: boolean;
    modifications: string;
    relic: string;

    owner: User;
    model?: Model | null;

    body: Body;
    neck: Neck;
    headstock: Headstock;
    fretboard: Fretboard;
    nut: Nut;
    frets: Frets;
    inlays: Inlays;
    bridge: Bridge;
    saddles: Saddles;
    switch: Switch;
    controls: Controls;
    tuning_machine: TuningMachine;
    string_tree: StringTree;
    neck_plate: NeckPlate;
    pickguard: Pickguard;
}

export interface Body {
    id: number;
    wood: string;
    contour: string;
    routing: string;
    finish: string;
    color: string;
}

export interface Neck {
    id: number;
    wood: string;
    finish: string;
    shape: string;
    scale_length: string;
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
    radius: string;
}

export interface Nut {
    id: number;
    width: string;
    material: string;
    locking: boolean;
}

export interface Frets {
    id: number;
    count: number;
    material: string;
    size: string;
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
    spacing: string;
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

export interface User {
    id: number;
    username: string;
    email: string;
    role: string;
    user_guitars: UserGuitar[];
}
