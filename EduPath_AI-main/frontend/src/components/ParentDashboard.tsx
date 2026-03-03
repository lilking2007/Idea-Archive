import React from 'react';

export function ParentDashboard() {
    const childStats = {
        name: 'Alex',
        studyTimeHours: 4.5,
        topicsCompleted: 12,
        totalTopics: 50,
        recentActivity: 'Completed Quiz: Algebra Basics (90%)'
    };

    const progressPercentage = (childStats.topicsCompleted / childStats.totalTopics) * 100;

    return (
        <div style={{ padding: '20px', backgroundColor: '#1e1e1e', borderRadius: '10px' }}>
            <h2 style={{ borderBottom: '1px solid #444', paddingBottom: '10px' }}>Parent Dashboard</h2>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginTop: '20px' }}>
                <div style={cardStyle}>
                    <h4>Study Time This Week</h4>
                    <p style={bigNumberStyle}>{childStats.studyTimeHours} hrs</p>
                </div>

                <div style={cardStyle}>
                    <h4>Topics Completed</h4>
                    <p style={bigNumberStyle}>{childStats.topicsCompleted}</p>
                    <div style={{ width: '100%', backgroundColor: '#333', height: '6px', borderRadius: '3px', marginTop: '10px' }}>
                        <div style={{ width: `${progressPercentage}%`, backgroundColor: '#4A90E2', height: '100%', borderRadius: '3px' }}></div>
                    </div>
                </div>

                <div style={cardStyle}>
                    <h4>Recent Activity</h4>
                    <p style={{ color: '#aaa', fontSize: '14px' }}>{childStats.recentActivity}</p>
                </div>
            </div>
        </div>
    );
}

const cardStyle = {
    backgroundColor: '#2a2a2a',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.3)'
};

const bigNumberStyle = {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#fff',
    margin: '10px 0'
};
