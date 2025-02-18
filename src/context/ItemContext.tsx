import { createContext, useContext, useState, ReactNode } from "react";
import { Model, UserGuitar } from "../types";

interface ItemContextType {
    item: Model | UserGuitar | null;
    setItem: (item: Model | UserGuitar | null) => void;
}

const ItemContext = createContext<ItemContextType | undefined>(undefined);

export const ItemProvider = ({ children }: { children: ReactNode }) => {
    const [item, setItem] = useState<Model | UserGuitar | null>(null);

    return (
        <ItemContext.Provider value={{ item, setItem }}>
            {children}
        </ItemContext.Provider>
    );
};

export const useItem = (): ItemContextType => {
    const context = useContext(ItemContext);
    if (!context) {
        throw new Error("useItem must be used within an ItemProvider");
    }
    return context;
};
