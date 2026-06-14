import { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [fontUrl, setFontUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [spacing, setSpacing] = useState(0); 

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/generate-font', formData, {
        responseType: 'blob',
      });

      const url = URL.createObjectURL(response.data);
      setFontUrl(url);

      const newFont = new FontFace('CustomHandwriting', `url(${url})`);
      await newFont.load();
      document.fonts.add(newFont);

    } catch (error) {
      console.error("Error generating font:", error);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '50px', fontFamily: 'sans-serif', maxWidth: '800px', margin: '0 auto' }}>
      <h1>AI Cursive Generator</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={loading} style={{ marginLeft: '10px' }}>
        {loading ? "Processing..." : "Generate Font"}
      </button>

      {fontUrl && (
        <div style={{ marginTop: '30px' }}>
          <h2>Test Your Font:</h2>
          
          <div style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#333', borderRadius: '8px', color: 'white' }}>
            <label style={{ display: 'block', marginBottom: '10px' }}>
              <strong>Adjust Letter Connection (CSS Tracking): {spacing}px</strong>
            </label>
            <input 
              type="range" 
              min="-15" 
              max="5" 
              step="0.5" 
              value={spacing} 
              onChange={(e) => setSpacing(e.target.value)} 
              style={{ width: '100%' }}
            />
          </div>

          <textarea 
            style={{ 
              fontFamily: 'CustomHandwriting', 
              fontSize: '40px', 
              width: '100%', 
              height: '150px',
              letterSpacing: `${spacing}px` 
            }}
            defaultValue="happy birthday sir"
          />
        </div>
      )}
    </div>
  );
}

export default App;