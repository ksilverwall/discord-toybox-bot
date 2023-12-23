resource "aws_ecs_cluster" "discord_toybox_bot" {
  name = "discord-toybox-bot"
}

resource "aws_iam_role" "discord_toybox_role" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_ecs_task_definition" "discord_toybox_task" {
  family                   = "discord-toybox-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  execution_role_arn = aws_iam_role.discord_toybox_role.arn

  container_definitions = jsonencode([
    {
      name  = "discord_toybox_bot",
      image = "${aws_ecr_repository.discord_toybox.repository_url}:latest",
      cpu   = 256,
      memory = 512,
      essential = true,
      portMappings = [
        {
          containerPort = 80,
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "discord_toybox_service" {
  name            = "discord-toybox-service"
  cluster         = aws_ecs_cluster.discord_toybox_bot.id
  task_definition = aws_ecs_task_definition.discord_toybox_task.arn
  launch_type     = "FARGATE"

  network_configuration {
    subnets = [aws_subnet.discord_toybox_1.id, aws_subnet.discord_toybox_2.id]
    security_groups = [aws_security_group.discord_toybox_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.discord_toybox_tg.arn
    container_name   = "discord_toybox_bot"
    container_port   = 80
  }

  desired_count = 1

  deployment_controller {
    type = "ECS"
  }
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
}
