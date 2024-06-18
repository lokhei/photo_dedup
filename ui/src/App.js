import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Dropzone from 'react-dropzone';
import './App.css';

function App() {
  const [clusters, setClusters] = useState({});
  const [selectedForDeletion, setSelectedForDeletion] = useState([]);
  const [directoryPath, setDirectoryPath] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [currentCluster, setCurrentCluster] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [similarityThreshold, setSimilarityThreshold] = useState(0.8); // Default threshold




  const getDuplicates = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:5000/get_duplicates?similarity_threshold=${similarityThreshold}`);
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
      setDirectoryPath("uploads/");
      handleSetDirectory();
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

  const openImage = (imagePath, cluster) => {
    setCurrentCluster(cluster);
    setCurrentIndex(cluster.indexOf(imagePath));
    setSelectedImage(imagePath);
  };

  const closeImage = () => {
    setSelectedImage(null);
    setCurrentCluster([]);
    setCurrentIndex(0);
  };

  const showPreviousImage = (e) => {
    e.stopPropagation(); // Prevent the modal from closing
    const newIndex = (currentIndex - 1 + currentCluster.length) % currentCluster.length;
    setCurrentIndex(newIndex);
    setSelectedImage(currentCluster[newIndex]);
  };

  const showNextImage = (e) => {
    e.stopPropagation(); // Prevent the modal from closing
    const newIndex = (currentIndex + 1) % currentCluster.length;
    setCurrentIndex(newIndex);
    setSelectedImage(currentCluster[newIndex]);
  };


  const handleThresholdChange = async (e) => {
    const newThreshold = e.target.value;
    setSimilarityThreshold(newThreshold);
  };
  return (
    <div className="App">
      <h1 className="title">Image Duplicates Deleter</h1>
      <Dropzone onDrop={uploadFiles}>
        {({ getRootProps, getInputProps }) => (
          <div {...getRootProps()} className="dropzone">
            <input {...getInputProps()} />
            <p>Drag and drop files here, or click to select files</p>
          </div>
        )}
      </Dropzone>

      <div className="input-container">
        <input
          type="text"
          placeholder="Enter directory path"
          value={directoryPath}
          onChange={(e) => setDirectoryPath(e.target.value)}
          className="input"
        />
        <button onClick={handleSetDirectory} className="button">Set Directory</button>
        <button onClick={getDuplicates} className="button">Group Images</button>
      </div>

      <div className="slider-container">
        <label htmlFor="similarityThreshold">Similarity Threshold: {similarityThreshold}</label>
        <input
          type="range"
          id="similarityThreshold"
          min="0"
          max="1"
          step="0.01"
          value={similarityThreshold}
          onChange={handleThresholdChange}
          className="slider"
        />
      </div>


      {loading ? (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading...</p>
        </div>
      ) : (
        <div>
          {Object.keys(clusters).map(clusterKey => (
            <div key={clusterKey}>
              <h2>Group {clusterKey}</h2>
              <div className="image-container">
                {clusters[clusterKey].map(imagePath => (
                  <div
                    key={imagePath}
                    onClick={() => toggleSelectImage(imagePath)}
                    className={`image-wrapper ${selectedForDeletion.includes(imagePath) ? 'selected' : ''}`}
                    onDoubleClick={() => openImage(imagePath, clusters[clusterKey])}
                  >
                    <img src={`http://localhost:5000/images/${imagePath}`} alt="" className="image" />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
      {selectedForDeletion.length > 0 && (
        <button onClick={handleDeleteSelected} className="delete-button">Delete Selected</button>
      )}

      {selectedImage && (
        <div className="modal" onClick={closeImage}>
          <span className="close" onClick={closeImage}>&times;</span>
          <span className="arrow left-arrow" onClick={showPreviousImage}>&#10094;</span>
          <img className="modal-content" src={`http://localhost:5000/images/${selectedImage}`} alt="" />
          <span className="arrow right-arrow" onClick={showNextImage}>&#10095;</span>
          <div className="caption">{selectedImage}</div>
        </div>
      )}
    </div>
  );
}

export default App;
