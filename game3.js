// React component (BSTVisualizer.jsx)
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BSTVisualizer = () => {
    const [currentFrame, setCurrentFrame] = useState('');
    const [animationFrames, setAnimationFrames] = useState([]);
    const [animating, setAnimating] = useState(false);
    const [currentExample, setCurrentExample] = useState(0);
    const [totalExamples, setTotalExamples] = useState(3);

    useEffect(() => {
        axios.get('http://localhost:5000/api/init').then(res => {
            setCurrentFrame(res.data.frame);
            setTotalExamples(res.data.totalExamples);
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

    const handleStart = () => {
        axios.get('http://localhost:5000/api/start').then(res => {
            setAnimationFrames(res.data.frames);
            setAnimating(true);
        });
    };

    const handleNext = () => {
        axios.get('http://localhost:5000/api/next').then(res => {
            setCurrentFrame(res.data.frame);
            setCurrentExample(res.data.currentExample);
        });
    };

    return (
        <div style={{ textAlign: 'center', padding: '20px' }}>
            <div style={{ margin: '20px' }}>
                <button 
                    onClick={handleStart}
                    disabled={animating}
                    style={buttonStyle(animating)}
                >
                    {animating ? 'Animating...' : 'Start Balancing'}
                </button>
                <button 
                    onClick={handleNext}
                    disabled={currentExample >= totalExamples - 1}
                    style={{ ...buttonStyle(false), marginLeft: '10px' }}
                >
                    Next Example
                </button>
            </div>
            
            <img 
                src={`data:image/png;base64,${currentFrame}`} 
                alt="BST Visualization"
                style={{ 
                    border: '2px solid #333',
                    borderRadius: '10px',
                    boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
                }}
            />
            
            <div style={{ marginTop: '20px', fontSize: '1.2em' }}>
                Example {currentExample + 1} of {totalExamples}
            </div>
        </div>
    );
};

const buttonStyle = (disabled) => ({
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: disabled ? '#cccccc' : '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: disabled ? 'not-allowed' : 'pointer',
    transition: 'background-color 0.3s'
});

export default BSTVisualizer;