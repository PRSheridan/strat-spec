import { createContext, useContext, useState, ReactNode } from "react";
import { Guitar } from "../types";

interface GuitarContextType {
    guitar: Guitar | null;
    setGuitar: (guitar: Guitar | null) => void;
}

const GuitarContext = createContext<GuitarContextType | undefined>(undefined);

export const GuitarProvider = ({ children }: { children: ReactNode }) => {
    const [guitar, setGuitar] = useState<Guitar | null>(null);

    return (
        <GuitarContext.Provider value={{ guitar, setGuitar }}>
            {children}
        </GuitarContext.Provider>
    );
};

export const useGuitar = (): GuitarContextType => {
    const context = useContext(GuitarContext);
    if (!context) {
        throw new Error("useGuitar must be used within a GuitarProvider");
    }
    return context;
};
