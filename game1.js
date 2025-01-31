import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TreeVisualizer = () => {
  const [currentFrame, setCurrentFrame] = useState('');
  const [animationFrames, setAnimationFrames] = useState([]);
  const [animating, setAnimating] = useState(false);

  useEffect(() => {
    // Load initial frame
    axios.get('http://localhost:5000/api/init').then(res => {
      setCurrentFrame(res.data.frame);
    });
  }, []);

  useEffect(() => {
    if (animating && animationFrames.length > 0) {
      const timer = setInterval(() => {
        setAnimationFrames(prev => {
          const [current, ...remaining] = prev;
          if (current) setCurrentFrame(current);
          if (remaining.length === 0) setAnimating(false);
          return remaining;
        });
      }, 500);
      return () => clearInterval(timer);
    }
  }, [animating, animationFrames]);

  const handleSolve = () => {
    axios.get('http://localhost:5000/api/solve').then(res => {
      setAnimationFrames(res.data.frames);
      setAnimating(true);
    });
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <div style={{ margin: '20px' }}>
        <button 
          onClick={handleSolve}
          disabled={animating}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: animating ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          {animating ? 'Animating...' : 'Show Solution'}
        </button>
      </div>
      
      <img 
        src={`data:image/png;base64,${currentFrame}`} 
        alt="tree visualization"
        style={{ border: '1px solid #ddd', borderRadius: '5px' }}
      />
    </div>
  );
};

export default TreeVisualizer;