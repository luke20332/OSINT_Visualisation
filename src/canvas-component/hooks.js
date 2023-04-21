import { useRef, useState } from "react";

export function useOnDraw() {
    const canvasRef = useRef(null);
    const [ctx, setCtx] = useState(null);

    function setCanvasRef(ref) {
        if(!ref) return;
        canvasRef.current = ref;
        const ctx = canvasRef.current.getContext('2d');
        setCtx(ctx);
    }

    function draw([x1, y1], [x2, y2]) {
        if (!ctx) return;
        ctx.beginPath();
        ctx.arc(x1, y1, 5, 0, 2 * Math.PI);
        ctx.fillStyle = "blue";
        ctx.fill();
    
        ctx.beginPath();
        ctx.arc(x2, y2, 5, 0, 2 * Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();
      }

    return {setCanvasRef, draw};
};