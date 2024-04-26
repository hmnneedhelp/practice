import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState([]);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:8000");
        setData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    

    fetchData();
  }, []);

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
        setUploading(false);
        window.location.reload()
      })
      .catch((error) => {
        console.error(error);
        setUploading(false);
      });
  };
  

  return (
    <div className="flex flex-row w-full">
      <div className="flex flex-row w-1/2 gap-2 flex-wrap">
        {data.map((image) =>
          image.id ? (
            <div
              key={image.id}
              className="flex items-center justify-start flex-col"
            >
              <img src={`http://localhost:8000/decodeimage/${image.id}`} />
              <div className="text-white flex flex-row">
                <p>id: </p>
                <p>{image.id}</p>
              </div>
            </div>
          ) : null
        )}
      </div>
      <div className="flex flex-col border-l w-1/2 mx-auto">
        <input
          type="file"
          className="w-1/2 hidden"
          id="input"
          onChange={handleFileChange}
        />
        <label
          className="w-1/2 h-12 mx-auto flex items-center justify-center bg-white"
          htmlFor="input"
        >
          <div className="w-full h-12 text-center flex items-center hover:cursor-pointer justify-center bg-white">
            Загрузить фото
          </div>
        </label>
        <button className="bg-white w-1/2 mt-5 mx-auto mb-2" onClick={handleUpload}>
          Upload File
        </button>
        {uploading ? (
          <p className="text-white text-center">Uploading...</p>
        ) : (
          <p className="text-white text-center">Ready to upload</p>
        )}
      </div>
    </div>
  );
}

export default App;
