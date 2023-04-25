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
        //circle on first point
        if (!ctx) return;
        ctx.beginPath();
        ctx.arc(x1, y1, 5, 0, 2 * Math.PI);
        ctx.fillStyle = "blue";
        ctx.fill();
        //circle on second point
        ctx.beginPath();
        ctx.arc(x2, y2, 5, 0, 2 * Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();

        //draw line
        const start = ((x1 + y1)/2);
        const end = ((x2 + y2)/2);
        ctx.beginPath();
        ctx.setLineDash([5, 5]);
        ctx.moveTo(start[0], start[1]);
        ctx.lineTo(end[0], end[1]);
        ctx.strokeStyle = "black";
        ctx.stroke();
      }

    return {setCanvasRef, draw};
};