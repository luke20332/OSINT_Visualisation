import { useOnDraw } from './hooks';
import map from "./NE1_LR_LC.png"

const Canvas = ({
    width,
    height
}) => {

    const setCanvasRef = useOnDraw();

    const handleClear = () => {
        const canvas = setCanvasRef.current;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    };

    return (
        <>
      <img src={map} className="Map" alt="world map" class="center" />
      <canvas
        width={width}
        height={height}
        style={canvasStyle}
        ref={setCanvasRef}
      />
      <button onClick={handleClear}>Clear map</button>
    </>
    );
}

export default Canvas;

const canvasStyle = {
    border: '1px solid black',
    position: 'absolute',
}