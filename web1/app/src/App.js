import React, { useRef, useEffect, useState } from "react";
import * as tf from "@tensorflow/tfjs";
import * as cocoSsd from "@tensorflow-models/coco-ssd";

export default function App() {
  const canvasRef = useRef(null);
  const imgRef = useRef(null);
  const [model, setModel] = useState(null);
  const [loading, setLoading] = useState(true);
  const [imageURL, setImageURL] = useState(null);

  
  useEffect(() => {
    const loadModel = async () => {
      const loadedModel = await cocoSsd.load();
      setModel(loadedModel);
      setLoading(false);
    };
    loadModel();
  }, []);

  
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setImageURL(url);
    }
  };

 
  useEffect(() => {
    const detect = async () => {
      if (model && imgRef.current) {
        const predictions = await model.detect(imgRef.current);

        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");

        canvas.width = imgRef.current.width;
        canvas.height = imgRef.current.height;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(imgRef.current, 0, 0);

        predictions.forEach((prediction) => {
          const [x, y, width, height] = prediction.bbox;

          ctx.strokeStyle = "#00FF00";
          ctx.lineWidth = 2;
          ctx.strokeRect(x, y, width, height);

          ctx.fillStyle = "#00FF00";
          ctx.font = "16px Arial";
          ctx.fillText(
            `${prediction.class} (${Math.round(prediction.score * 100)}%)`,
            x,
            y > 10 ? y - 5 : 10
          );
        });
      }
    };

    if (imageURL) {
      const img = imgRef.current;
      img.onload = detect;
    }
  }, [model, imageURL]);

  return (
    <div className="flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">
        Image Object Detection (TensorFlow.js)
      </h1>

      {loading && <p>Loading model...</p>}

      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        className="mb-4"
      />

      <div className="relative">
        {imageURL && (
          <>
            <img
              ref={imgRef}
              src={imageURL}
              alt="Uploaded"
              className="hidden"
            />
            <canvas
              ref={canvasRef}
              className="rounded-2xl shadow-lg"
            />
          </>
        )}
      </div>
    </div>
  );
}



