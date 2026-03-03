import { Module } from '@nestjs/common';
import { RoadmapsModule } from './roadmaps/roadmaps.module';
import { UsersModule } from './users/users.module';
import { AuthModule } from './auth/auth.module';

@Module({
    imports: [RoadmapsModule, UsersModule, AuthModule],
    controllers: [],
    providers: [],
})
export class AppModule { }
