import React, { useState } from 'react';
import JSZip from 'jszip';
import Dashboard from './Dashboard';


const Home = () => {
  const [selectedZipFile, setSelectedZipFile] = useState(null);
  const [selectedCSVFile, setSelectedCSVFile] = useState(null);
  const [showDashBoard ,  setShowDashBoard] = useState(false);
  const [stopProcessing , setstopProcessing] = useState(false);

  const handleZipFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedZipFile(file);
  };

  const handleCSVFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedCSVFile(file);
  };

  const handleUpload = async () => {
    if (!selectedZipFile || !selectedCSVFile) {
      return;
    }

    try {
      setShowDashBoard(true);
      const zip = new JSZip();
      await zip.loadAsync(selectedZipFile);

      const files = [];
      zip.forEach(async (relativePath, file) => {
        const content = await file.async('uint8array');
        files.push({ path: relativePath, content });
      });

      const formData = new FormData();
      formData.append('zipFile', selectedZipFile);
      formData.append('csvFile', selectedCSVFile);

      const response = await fetch('http://localhost:3001/api/upload', {
        method: 'POST',
        body: formData,
      });

      // Handle the response from the backend
      if (response.ok) {
        console.log('Files uploaded successfully.');
        setShowDashBoard(true);
        var url = 'http://localhost:5601/app/dashboards#/list?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now%2Fd,to:now%2Fd))'

        if(window.confirm("View Dashboard")){
          window.open(url);
       }
        
      } else {
        console.error('Failed to upload files.');
      }
    } catch (error) {
      console.error('Error during file upload:', error);
    }
  };

  const stopProcess = async () => {
    try{
      const response = await fetch('http://localhost:3001/api/stopProcess', {
          method: 'POST'
        });
      if(response.ok){
        console.log("Stoped succesfully");
        setstopProcessing(true);
      }
      else{
        console.log("Failed to stop program")
      }
    }catch(error){
      console.error('Error during fstoping program:', error);
    }
  };
  
  const newProcess =()=>{
    setShowDashBoard(false);
    setstopProcessing(false);
  }

  const downloadData= async ()=>{
    try{
      const response = await fetch('http://localhost:3001/api/downloadData', {
          method: 'POST'
        });
      if(response.ok){
        console.log("Downloaded succesfully");
        alert("Downloaded Succesfully")
      }
      else{
        console.log("Failed to stop program")
      }
    }catch(error){
      console.error('Error during fstoping program:', error);
    }
  }

  return (
    <div className="container">
      {!showDashBoard && <div>
        <h1>File Upload</h1>
        <div className="mb-3">
          <label htmlFor="zipFileInput" className="form-label">
            Select a zip file:
          </label>
          <input
            type="file"
            className="form-control"
            id="zipFileInput"
            onChange={handleZipFileChange}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="csvFileInput" className="form-label">
            Select a CSV file:
          </label>
          <input
            type="file"
            className="form-control"
            id="csvFileInput"
            onChange={handleCSVFileChange}
          />
        </div>
        <button className="btn btn-primary" onClick={handleUpload}>
          Upload Files
        </button>
      </div>}
      <div>
        {showDashBoard && 
        <div>
          <Dashboard/>
          {!stopProcessing &&
          <button className="btn btn-primary" onClick={stopProcess}>
            Stop Process
          </button>}
          {stopProcessing && 
          <div>
          <button className="btn btn-primary" onClick={newProcess}>
            New Process
          </button> </div> &&
          <div>
          <button className="btn btn-primary" onClick={downloadData}>
          Download Data
          </button></div>
          }
        </div>
        }
      </div>
    </div>
  );
};

export default Home;
