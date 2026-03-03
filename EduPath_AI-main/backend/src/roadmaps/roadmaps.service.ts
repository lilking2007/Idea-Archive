import { Injectable } from '@nestjs/common';

export interface RoadmapNode {
    id: string;
    title: string;
    description: string;
    estimatedTime: number; // minutes
    status: 'locked' | 'in-progress' | 'completed';
    resources: { type: 'video' | 'article' | 'quiz', url: string, title: string }[];
}

export interface Roadmap {
    id: string;
    subject: string;
    grade: number;
    nodes: RoadmapNode[];
}

@Injectable()
export class RoadmapsService {
    private roadmaps: Roadmap[] = [];

    generateRoadmap(dto: { grade: number; subject: string; country: string }): Roadmap {
        // Mock algorithm for curriculum generation
        // In a real app, this would query a database of curriculum standards

        const roadmapId = Math.random().toString(36).substring(7);
        const nodes: RoadmapNode[] = [
            {
                id: 'node-1',
                title: `Introduction to ${dto.grade}th Grade ${dto.subject}`,
                description: 'Foundational concepts overview.',
                estimatedTime: 15,
                status: 'in-progress',
                resources: [
                    { type: 'video', title: 'Video Intro', url: 'https://youtube.com/example' },
                    { type: 'quiz', title: 'Baseline Assessment', url: '/quiz/1' }
                ]
            },
            {
                id: 'node-2',
                title: 'Core Concept 1',
                description: 'First major topic of the year.',
                estimatedTime: 30,
                status: 'locked',
                resources: []
            },
            {
                id: 'node-3',
                title: 'Core Concept 2',
                description: 'Second major topic of the year.',
                estimatedTime: 45,
                status: 'locked',
                resources: []
            }
        ];

        const newRoadmap: Roadmap = {
            id: roadmapId,
            subject: dto.subject,
            grade: dto.grade,
            nodes
        };

        this.roadmaps.push(newRoadmap);
        return newRoadmap;
    }

    findOne(id: string) {
        return this.roadmaps.find(r => r.id === id);
    }
}
