import { useOnDraw } from './hooks';
import map from "./wrld-15-crop.jpg"

const Canvas = ({
    width,
    height
}) => {

    const setCanvasRef = useOnDraw();

    return (
        <>
      <img src={map} className="Map" alt="world map" class="center" />
      <canvas
        width={width}
        height={height}
        style={canvasStyle}
        ref={setCanvasRef}
      />
    </>
    );
}

export default Canvas;

const canvasStyle = {
    border: '1px solid black',
    position: 'absolute',
}