import React, { useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import axios from "axios";

function App() {
  const [data, setData] = useState({});
  const [decodedImage, setDecodedImage] = useState("");
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:8000");
        console.log(response.data);
        setData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData(); // Вызов асинхронной функции fetchData внутри useEffect
  }, []); // Пустой массив зависимостей, чтобы useEffect вызывался только один раз

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = () => {
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    axios.post('http://localhost:8000/encodeimage', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
      .then((response) => {
        setUploadedFile(response.data);
        setUploading(false);
      })
      .catch((error) => {
        console.error(error);
        setUploading(false);
      });
  };

  return (
    <div className="flex flex-row w-full">
      <div className="flex flex-row w-1/2 border-r h-full gap-2">
        {Array.isArray(data) &&
          data.map((id) => (
            <div key={id} className="flex items-center justify-start flex-col">
              <img src={`http://localhost:8000/decodeimage/${id.id}`} />
              <div className="text-white flex flex-row">
                <p>id: </p>
                <p>{id.id}</p>
              </div>
            </div>
          ))}
      </div>
      <div className="flex flex-col w-1/2 mx-auto">
        <input type="file" className="w-1/2 hidden" id="input" onChange={()=>handleFileChange()} />
        <label className="w-1/2 h-12 mx-auto flex items-center justify-center bg-white" htmlFor="input" onChange={()=>handleFileChange()}>
            <div className="w-1/2 h-12 text-center flex items-center hover:cursor-pointer justify-center bg-white" onChange={()=>handleFileChange()}>Загрузить фото</div>
        </label>
        <button className="bg-white w-1/2 mt-5 mx-auto" onClick={handleUpload}>Upload File</button>
        {uploading ? (
          <p className="text-white">Uploading...</p>
        ) : (
          <p className="text-white">
            {uploadedFile
              ? `File uploaded successfully: ${uploadedFile}`
              : "Ready to upload"}
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
