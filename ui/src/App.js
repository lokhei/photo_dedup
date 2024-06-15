import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Dropzone from 'react-dropzone';

function App() {
  const [clusters, setClusters] = useState({});
  const [selectedForDeletion, setSelectedForDeletion] = useState([]);
  const [directoryPath, setDirectoryPath] = useState('');
  const [loading, setLoading] = useState(false);

  const getDuplicates = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:5000/get_duplicates');
      setClusters(response.data);
    } catch (error) {
      console.error('Error fetching duplicates:', error);
    }
    setLoading(false);
  };


  const handleSetDirectory = async () => {
    try {
      await axios.post('http://localhost:5000/set_directory', { directory_path: directoryPath });
    } catch (error) {
      console.error('Error setting directory:', error);
    }
  };

  const uploadFiles = async (acceptedFiles) => {
    const formData = new FormData();
    acceptedFiles.forEach(file => formData.append('images', file));

    try {
      await axios.post('http://localhost:5000/upload', formData);
    } catch (error) {
      console.error('Error uploading images:', error);
    }
  };

  const toggleSelectImage = (imagePath) => {
    setSelectedForDeletion(prev => {
      if (prev.includes(imagePath)) {
        return prev.filter(path => path !== imagePath);
      } else {
        return [...prev, imagePath];
      }
    });
  };

  const handleDeleteSelected = async () => {
    try {
      await axios.post('http://localhost:5000/delete', { image_paths: selectedForDeletion });
      setSelectedForDeletion([]);
      getDuplicates();
    } catch (error) {
      console.error('Error deleting images:', error);
    }
  };

  return (
    <div className="App">
      <h1>Image Cluster Deleter</h1>
      <Dropzone onDrop={uploadFiles}>
        {({ getRootProps, getInputProps }) => (
          <div {...getRootProps()} style={{ border: '2px dashed gray', padding: '20px', cursor: 'pointer' }}>
            <input {...getInputProps()} />
            <p>Drag and drop files here, or click to select files</p>
          </div>
        )}
      </Dropzone>

      <input
        type="text"
        placeholder="Enter directory path"
        value={directoryPath}
        onChange={(e) => setDirectoryPath(e.target.value)}
        style={{ width: '300px', marginRight: '10px' }}
      />
      <button onClick={handleSetDirectory}>Set Directory</button>
    
      <button onClick={getDuplicates} style={{ margin: '20px' }}>Group Images</button>
      {loading ? (
        <p>Loading...</p>  // Show loading sign
      ) : (
      <div>
        {Object.keys(clusters).map(clusterKey => (
          <div key={clusterKey}>
            <h2>Cluster {clusterKey}</h2>
            <div style={{ display: 'flex', flexWrap: 'wrap' }}>
              {clusters[clusterKey].map(imagePath => (
                <div
                  key={imagePath}
                  onClick={() => toggleSelectImage(imagePath)}
                  style={{
                    border: selectedForDeletion.includes(imagePath) ? '2px solid red' : '2px solid black',
                    margin: '5px',
                    cursor: 'pointer'
                  }}
                >
                  <img src={`http://localhost:5000/${imagePath}`} alt="" style={{ width: '150px', height: '150px' }} />
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      )}
      {selectedForDeletion.length > 0 && (
        <button onClick={handleDeleteSelected}>Delete Selected</button>
      )}
    </div>
  );
}

export default App;
