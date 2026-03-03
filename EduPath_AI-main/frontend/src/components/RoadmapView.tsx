import React, { useState, useEffect } from 'react';
import './RoadmapView.css';

interface Node {
    id: string;
    title: string;
    description: string;
    status: 'locked' | 'in-progress' | 'completed';
}

export function RoadmapView() {
    // Mock data - would normally fetch from API
    const [nodes, setNodes] = useState<Node[]>([
        { id: '1', title: 'Calculus I: Limits', description: 'Introduction to limits and continuity.', status: 'completed' },
        { id: '2', title: 'Calculus I: Derivatives', description: 'The definition of the derivative.', status: 'in-progress' },
        { id: '3', title: 'Calculus I: Integrals', description: 'Computing areas under curves.', status: 'locked' },
    ]);

    return (
        <div className="roadmap-container">
            <h2>My Learning Path: Mathematics</h2>
            {nodes.map((node) => (
                <div key={node.id} className={`roadmap-node ${node.status}`}>
                    <div className={`node-status status-${node.status}`}>
                        {node.status.toUpperCase().replace('-', ' ')}
                    </div>
                    <h3>{node.title}</h3>
                    <p>{node.description}</p>
                </div>
            ))}
        </div>
    );
}
