import { Test, TestingModule } from '@nestjs/testing';
import { RoadmapsService } from './roadmaps.service';

describe('RoadmapsService', () => {
    let service: RoadmapsService;

    beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
            providers: [RoadmapsService],
        }).compile();

        service = module.get<RoadmapsService>(RoadmapsService);
    });

    it('should be defined', () => {
        expect(service).toBeDefined();
    });

    it('should generate a roadmap with correct structure', () => {
        const roadmap = service.generateRoadmap({
            grade: 5,
            subject: 'Math',
            country: 'USA'
        });

        expect(roadmap).toHaveProperty('id');
        expect(roadmap.subject).toBe('Math');
        expect(roadmap.nodes.length).toBeGreaterThan(0);
        expect(roadmap.nodes[0].status).toBe('in-progress');
    });
});
