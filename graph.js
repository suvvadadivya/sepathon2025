import React, { useEffect, useRef, useState } from 'react';

const GameComponent = () => {
    const [gameState, setGameState] = useState({
        current_problem: 0,
        game_over: false,
        animating: false
    });
    const canvasRef = useRef(null);
    const animationRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const imageData = new ImageData(800, 600);
        
        const fetchFrame = async () => {
            try {
                const response = await fetch('http://localhost:5000/frame');
                const buffer = await response.arrayBuffer();
                const bytes = new Uint8ClampedArray(buffer);
                imageData.data.set(bytes);
                ctx.putImageData(imageData, 0, 0);
            } catch (error) {
                console.error('Error fetching frame:', error);
            }
            animationRef.current = requestAnimationFrame(fetchFrame);
        };

        const fetchState = async () => {
            try {
                const response = await fetch('http://localhost:5000/state');
                const state = await response.json();
                setGameState(state);
            } catch (error) {
                console.error('Error fetching state:', error);
            }
        };

        animationRef.current = requestAnimationFrame(fetchFrame);
        const stateInterval = setInterval(fetchState, 500);

        return () => {
            cancelAnimationFrame(animationRef.current);
            clearInterval(stateInterval);
        };
    }, []);

    const handleStart = async () => {
        await fetch('http://localhost:5000/start', { method: 'POST' });
    };

    const handleNext = async () => {
        await fetch('http://localhost:5000/next', { method: 'POST' });
    };

    return (
        <div style={{ textAlign: 'center' }}>
            <canvas 
                ref={canvasRef}
                width={800}
                height={600}
                style={{ border: '1px solid #ccc', margin: '20px' }}
            />
            <div>
                <button 
                    onClick={handleStart}
                    disabled={gameState.animating || gameState.game_over}
                    style={{ margin: '0 10px', padding: '10px 20px' }}
                >
                    Start
                </button>
                <button 
                    onClick={handleNext}
                    disabled={gameState.current_problem >= 2 || gameState.animating}
                    style={{ margin: '0 10px', padding: '10px 20px' }}
                >
                    Next
                </button>
            </div>
            {gameState.game_over && (
                <div style={{ color: 'red', fontSize: '24px', marginTop: '20px' }}>
                    Game Over!
                </div>
            )}
            {gameState.current_problem >= 2 && !gameState.game_over && (
                <div style={{ color: 'green', fontSize: '24px', marginTop: '20px' }}>
                    Success! All problems solved!
                </div>
            )}
        </div>
    );
};

export default GameComponent;