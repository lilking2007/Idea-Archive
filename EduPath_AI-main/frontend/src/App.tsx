import React, { useState } from 'react';
import { RoadmapView } from './components/RoadmapView';
import { ParentDashboard } from './components/ParentDashboard';

function App() {
    const [view, setView] = useState<'student' | 'parent'>('student');

    return (
        <div style={{ fontFamily: 'Inter, sans-serif', maxWidth: '1000px', margin: '0 auto', padding: '20px' }}>
            <header style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '40px',
                padding: '20px',
                borderBottom: '1px solid #333'
            }}>
                <div>
                    <h1 style={{ color: '#4A90E2', margin: 0 }}>EduPath AI</h1>
                    <p style={{ color: '#888', margin: '5px 0 0' }}>Personalized Learning Platform</p>
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                    <button
                        onClick={() => setView('student')}
                        style={view === 'student' ? activeButtonStyle : buttonStyle}>
                        Student View
                    </button>
                    <button
                        onClick={() => setView('parent')}
                        style={view === 'parent' ? activeButtonStyle : buttonStyle}>
                        Parent Dashboard
                    </button>
                </div>
            </header>

            <main>
                {view === 'student' ? <RoadmapView /> : <ParentDashboard />}
            </main>
        </div>
    );
}

const buttonStyle = {
    padding: '10px 20px',
    borderRadius: '6px',
    border: '1px solid #444',
    background: 'transparent',
    color: '#aaa',
    cursor: 'pointer'
};

const activeButtonStyle = {
    ...buttonStyle,
    background: '#4A90E2',
    color: '#fff',
    border: '1px solid #4A90E2'
};

export default App;
