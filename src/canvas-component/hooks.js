import { useRef } from "react";

export function useOnDraw() {
    const canvasRef = useRef(null);

    function setCanvasRef() {
        if(!ref) return;
        canvasRef.current = ref;
    }
    
    return setCanvasRef;
};