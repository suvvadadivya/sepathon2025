import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GameViewer = () => {
  const [currentFrame, setCurrentFrame] = useState('');
  const [problemNum, setProblemNum] = useState(0);
  const [animationFrames, setAnimationFrames] = useState([]);
  const [animating, setAnimating] = useState(false);

  useEffect(() => {
    // Load initial frame
    axios.get('/api/init').then(res => {
      setCurrentFrame(res.data.frame);
      setProblemNum(res.data.problem);
    });
  }, []);

  useEffect(() => {
    if (animating && animationFrames.length > 0) {
      const timer = setInterval(() => {
        setAnimationFrames(prev => {
          const [current, ...remaining] = prev;
          setCurrentFrame(current);
          if (remaining.length === 0) setAnimating(false);
          return remaining;
        });
      }, 500);
      return () => clearInterval(timer);
    }
  }, [animating, animationFrames]);

  const handleStart = () => {
    axios.get('/api/start').then(res => {
      setAnimationFrames(res.data.frames);
      setAnimating(true);
    });
  };

  const handleNext = () => {
    axios.get('/api/next').then(res => {
      setCurrentFrame(res.data.frame);
      setProblemNum(res.data.problem);
    });
  };

  return (
    <div>
      <div style={{ position: 'relative' }}>
        <img 
          src={`data:image/png;base64,${currentFrame}`} 
          alt="game frame"
          style={{ border: '1px solid black' }}
        />
        <div style={{ position: 'absolute', bottom: 10, left: '50%', transform: 'translateX(-50%)' }}>
          <button onClick={handleStart} disabled={animating}>Start</button>
          <button 
            onClick={handleNext} 
            disabled={problemNum >= 2 || animating}
            style={{ marginLeft: 10 }}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default GameViewer;