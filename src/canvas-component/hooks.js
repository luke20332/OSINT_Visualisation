import { useRef } from "react";

export function useOnDraw() {
    const canvasRef = useRef(null);

    function setCanvasRef(ref) {
        if(!ref) return;
        canvasRef.current = ref;
        getPixelLocation();
    }

    function getPixelLocation() {
        const mouseListener = (e) => {
            console.log({x: e.clientX, y : e.clientY});
        }
        window.addEventListener("pixelLocation", mouseListener);
    }
    
    return setCanvasRef;
};