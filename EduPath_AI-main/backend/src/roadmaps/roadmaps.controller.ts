import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { RoadmapsService } from './roadmaps.service';

@Controller('roadmaps')
export class RoadmapsController {
    constructor(privatereadonly roadmapsService: RoadmapsService) { }

    @Post('generate')
    generateRoadmap(@Body() createRoadmapDto: { grade: number; subject: string; country: string }) {
        return this.roadmapsService.generateRoadmap(createRoadmapDto);
    }

    @Get(':id')
    findOne(@Param('id') id: string) {
        return this.roadmapsService.findOne(id);
    }
}
