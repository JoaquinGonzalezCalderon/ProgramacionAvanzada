import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { UserModels } from './users/entities/user.entity'

@Module({
  imports: [UserModels],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule { }
